# FIXME:https://engweb.commvault.com/engtools/defect/215340
# FIXME:https://engweb.commvault.com/engtools/defect/215230
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing instance operations.

Instances and Instance are 2 classes defined in this file.

Instances:  Class for representing all the instances associated with a specific agent

Instance:   Class for a single instance selected for an agent,
and to perform operations on that instance


Instances:
    __init__(agent_object)          --  initialise object of Instances class associated with
    the specified agent

    __str__()                       --  returns all the instances associated with the agent

    __repr__()                      --  returns the string for the object of the Instances class

    __len__()                       --  returns the number of instances associated to the Agent

    __getitem__()                   --  returns the name of the instance for the given instance ID
    or the details for the given instance name

    _get_instances()                --  gets all the instances associated with the agent specified

    all_instances()                 --  returns the dict of all the instances

    has_instance(instance_name)     --  checks if a instance exists with the given name or not

    get(instance_name)              --  returns the Instance class object
    of the input backup set name

    add_informix_instance()         --  adds new Informix Instance to given Client

    delete()                        --  deletes the instance specified by the instance_name
    from the agent.

    add_sybase_instance()           --  To add sybase server instance

    add_big_data_apps_instance()    --  To add an instance with the big data apps agent specified

    add_s3_instance()               --  Method to add a new s3 instance

    add_azure_instance()            --  Method to add a new azure instance

    add_oraclecloud_instance()      --  Method to add a new oracle cloud instance

    add_openstack_instance()        --  Method to add a new openstack instance

    delete_cloud_apps_instance()    --  Method to delete an instance from cloud apps agent

    refresh()                       --  refresh the instances associated with the agent


Instance:
    __init__()                      --  initialise object of Instance with the specified instance
    name and id, and associated to the specified agent

    __repr__()                      --  return the instance name, the object is associated with

    _get_instance_id()              --  method to get the instance id, if not specified in __init__

    _get_instance_properties()      --  method to get the properties of the instance

    _process_update_response()      --  updates the instance properties

    _process_restore_response()     --  processes the restore request sent to server
    and returns the restore job object

    _filter_paths()                 --  filters the path as per the OS, and the Agent

    _impersonation_json()           --  setter for impersonation Property

    _restore_browse_option_json()   --  setter for  browse option  property in restore

    _restore_commonOptions_json()   --  setter for common options property in restore

    _restore_destination_json()     --  setter for destination options property in restore

    _restore_fileoption_json()      --  setter for file option property in restore

    _restore_destination_json()     --  setter for destination property in restore

    _restore_volume_rst_option_json()  --  setter for the volumeRst restore option in restore JSON

    _restore_json()                 --  returns the apppropriate JSON request to pass for either
    Restore In-Place or Out-of-Place operation

    _restore_in_place()             --  Restores the files/folders specified in the
    input paths list to the same location

    _restore_out_of_place()         --  Restores the files/folders specified in the input paths
    list to the input client, at the specified destination location

    _task()                         --  the task dict used while restore/backup job

    _restore_sub_task()             --  the restore job specific sub task dict used to form
    restore json

    instance_id()                   --  id of this instance

    instance_name()                 --  name of this instance

    browse()                        --  browse the content of the instance

    find()                          --  find content in the instance

    refresh()                       --  refresh the properties of the instance

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode
from past.builtins import basestring

from .job import Job
from .subclient import Subclients
from .constants import AppIDAType
from .exception import SDKException
from .schedules import SchedulePattern, Schedule


class Instances(object):
    """Class for getting all the instances associated with a client."""

    def __init__(self, agent_object):
        """Initialize object of the Instances class.

            Args:
                agent_object (object)  --  instance of the Agent class

            Returns:
                object - instance of the Instances class
        """
        self._agent_object = agent_object
        self._client_object = self._agent_object._client_object

        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._INSTANCES = self._services['GET_ALL_INSTANCES'] % (
            self._client_object.client_id
        )

        self._instances = None
        self.refresh()

        from .instances.vsinstance import VirtualServerInstance
        from .instances.cainstance import CloudAppsInstance
        from .instances.sqlinstance import SQLServerInstance
        from .instances.hanainstance import SAPHANAInstance
        from .instances.oracleinstance import OracleInstance
        from .instances.sybaseinstance import SybaseInstance
        from .instances.saporacleinstance import SAPOracleInstance
        from .instances.mysqlinstance import MYSQLInstance
        from .instances.lndbinstance import LNDBInstance
        from .instances.postgresinstance import PostgreSQLInstance
        from .instances.informixinstance import InformixInstance

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        self._instances_dict = {
            'virtual server': VirtualServerInstance,
            'cloud apps': CloudAppsInstance,
            'sql server': SQLServerInstance,
            'sap hana': SAPHANAInstance,
            'oracle': OracleInstance,
            'sybase': SybaseInstance,
            'sap for oracle': SAPOracleInstance,
            'mysql': MYSQLInstance,
            'notes database': LNDBInstance,
            'postgresql': PostgreSQLInstance,
            'informix': InformixInstance
        }

    def __str__(self):
        """Representation string consisting of all instances of the agent of a client.

            Returns:
                str - string of all the instances of an agent of a client
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Instance', 'Agent', 'Client'
        )

        for index, instance in enumerate(self._instances):
            sub_str = '{:^5}\t{:20}\t{:20}\t{:20}\n'.format(
                index + 1,
                instance,
                self._agent_object.agent_name,
                self._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Instances class."""
        return "Instances class instance for Agent: '{0}'".format(self._agent_object.agent_name)

    def __len__(self):
        """Returns the number of the instances associated to the Agent."""
        return len(self.all_instances)

    def __getitem__(self, value):
        """Returns the name of the instance for the given instance ID or
            the details of the instance for given instance Name.

            Args:
                value   (str / int)     --  Name or ID of the instance

            Returns:
                str     -   name of the instance, if the instance id was given

                dict    -   dict of details of the instance, if instance name was given

            Raises:
                IndexError:
                    no instance exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_instances:
            return self.all_instances[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_instances.items())
                )[0][0]
            except IndexError:
                raise IndexError('No instance exists with the given Name / Id')

    def _get_instances(self):
        """Gets all the instances associated to the agent specified by agent_object.

            Returns:
                dict - consists of all instances of the agent
                    {
                         "instance1_name": instance1_id,
                         "instance2_name": instance2_id
                    }

            Raises:
                SDKException:
                    if failed to get instances

                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._INSTANCES)

        if flag:
            if response.json():
                if 'instanceProperties' in response.json():
                    return_dict = {}

                    for dictionary in response.json()['instanceProperties']:

                        agent = dictionary['instance']['appName'].lower()

                        if self._agent_object.agent_name in agent:
                            temp_name = dictionary['instance']['instanceName'].lower()
                            temp_id = str(dictionary['instance']['instanceId']).lower()
                            return_dict[temp_name] = temp_id

                    return return_dict
                elif 'errors' in response.json():
                    error = response.json()['errors'][0]
                    error_string = error['errorString']
                    raise SDKException('Instance', '102', error_string)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_instances(self):
        """Returns dict of all the instances associated with the agent

            dict - consists of all instances of the agent
                    {
                         "instance1_name": instance1_id,
                         "instance2_name": instance2_id
                    }

        """
        return self._instances

    def has_instance(self, instance_name):
        """Checks if a instance exists for the agent with the input instance name.

            Args:
                instance_name (str)  --  name of the instance

            Returns:
                bool - boolean output whether the instance exists for the agent or not

            Raises:
                SDKException:
                    if type of the instance name argument is not string
        """
        if not isinstance(instance_name, basestring):
            raise SDKException('Instance', '101')

        return self._instances and instance_name.lower() in self._instances

    def get(self, instance_name):
        """Returns a instance object of the specified instance name.

            Args:
                instance_name (str)  --  name of the instance

            Returns:
                object - instance of the Instance class for the given instance name

            Raises:
                SDKException:
                    if type of the instance name argument is not string

                    if no instance exists with the given name
        """
        if not isinstance(instance_name, basestring):
            raise SDKException('Instance', '101')
        else:
            instance_name = instance_name.lower()

            agent_name = self._agent_object.agent_name

            if self.has_instance(instance_name):
                if agent_name in self._instances_dict:
                    return self._instances_dict[agent_name](
                        self._agent_object, instance_name, self._instances[instance_name]
                    )
                else:
                    return Instance(
                        self._agent_object, instance_name, self._instances[instance_name]
                    )

            raise SDKException(
                'Instance', '102', 'No instance exists with name: "{0}"'.format(instance_name)
            )

    def add_informix_instance(self, informix_options):
        """Adds new Informix Instance to given Client
            Args:
                Dictionary of informix instance creation options:
                    Example:
                       informix_options = {
                            'instance_name': 'ol_informix1210',
                            'onconfig_file': 'onconfig.ol_informix1210',
                            'sql_host_file': 'C:\\IBM\\etc\\sqlhosts.ol_informix1210',
                            'informix_dir': 'C:\\IBM',
                            'user_name':'informix',
                            'domain_name':'test_vm',
                            'password':'commvault!12',
                            'storage_policy':'gk_pg_policy',
                            'description':'created from automation'
                        }

            Returns:
                object - instance of the Instance class

            Raises:
                SDKException:
                    if None value in informix options

                    if Informix instance with same name already exists

                    if given storage policy does not exists in commcell
        """
        if None in informix_options.values():
            raise SDKException(
                'Instance',
                '102',
                "One of the informix parameter is None so cannot proceed with instance creation")

        if self.has_instance(informix_options["instance_name"]):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(
                    informix_options["instance_name"])
            )

        if not self._commcell_object.storage_policies.has_policy(
                informix_options["storage_policy"]):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    informix_options["storage_policy"])
            )
        password = b64encode(informix_options["password"].encode()).decode()

        request_json = {
            "instanceProperties": {
                "description": informix_options['description'],
                "instance": {
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": informix_options["instance_name"],
                    "appName": "Informix Database"
                },
                "informixInstance": {
                    "onConfigFile": informix_options["onconfig_file"],
                    "sqlHostfile": informix_options["sql_host_file"],
                    "informixDir": informix_options["informix_dir"],
                    "informixUser": {
                        "password": password,
                        "domainName": informix_options["domain_name"],
                        "userName": informix_options["user_name"]
                    },
                    "informixStorageDevice": {
                        "dataBackupStoragePolicy": {
                            "storagePolicyName": informix_options["storage_policy"]
                        },
                        "deDuplicationOptions": {},
                        "logBackupStoragePolicy": {
                            "storagePolicyName": informix_options["storage_policy"]
                        },
                        "commandLineStoragePolicy": {
                            "storagePolicyName": informix_options["storage_policy"]
                        }
                    }
                }
            }
        }

        add_instance = self._commcell_object._services['ADD_INSTANCE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_instance, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'].get('errorCode')

                if error_code != 0:
                    error_string = response.json()['response'].get('errorString')
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    if 'entity' in response.json()['response']:
                        self.refresh()
                        return self._instances_dict[self._agent_object.agent_name](
                            self._agent_object,
                            response.json()['response']['entity'].get('instanceName'),
                            response.json()['response']['entity'].get('instanceId')
                        )
                    else:
                        raise SDKException(
                            'Instance',
                            '102',
                            'Unable to get instance name and id'
                        )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def delete(self, instance_name):
        """Deletes the instance specified by the instance_name from the agent.

            Args:
                instance_name (str)  --  name of the instance to remove from the agent

            Raises:
                SDKException:
                    if type of the instance name argument is not string

                    if failed to delete instance

                    if response is empty

                    if response is not success

                    if no instance exists with the given name
        """
        if not isinstance(instance_name, basestring):
            raise SDKException('Instance', '101')
        else:
            instance_name = instance_name.lower()

        if self.has_instance(instance_name):
            delete_instance_service = self._commcell_object._services['INSTANCE'] % (
                self._instances.get(instance_name)
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', delete_instance_service
            )

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value.get('errorCode'))
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = response_value['errorString']

                        if error_message:
                            o_str = 'Failed to delete instance\nError: "{0}"'
                            raise SDKException('Instance', '102', o_str.format(error_message))
                        else:
                            if error_code == '0':
                                # initialize the instances again
                                # so the instance object has all the instances
                                self.refresh()
                            else:
                                o_str = ('Failed to delete instance with Error Code: "{0}"\n'
                                         'Please check the documentation for '
                                         'more details on the error')
                                raise SDKException('Instance', '102', o_str.format(error_code))
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Instance', '102', 'No Instance exists with name: {0}'.format(instance_name)
            )

    def add_sybase_instance(self, sybase_options):
        """
            Method to Add new Sybase Instance to given Client
            Args:
                Dictionary of sybase instance creation options:
                    Example:
                       sybase_options = {
                            'instance_name': 'SAISYB',
                            'sybase_ocs': 'OCS-16_0',
                            'sybase_ase': 'ASE-16_0',
                            'backup_server': 'SAISYB_BS',
                            'sybase_home':'C:\\SAP',
                            'config_file':'C:\\SAP\\SAISYB.cfg',
                            'enable_auto_discovery':True,
                            'shared_memory_directory':'C:\\SAP\\ASE-16_0',
                            'storage_policy':'sai-sp',
                            'sa_username':'sa',
                            'sa_password':'commvault!12',
                            'localadmin_username':'saisyb\\administrator',
                            'localadmin_password':'commvault!12'
                        }
            Raises:
                SDKException:
                    if None value in sybase options

                    if Sybase instance with same name already exists

                    if given storage policy does not exists in commcell

        """

        if None in sybase_options.values():
            raise SDKException(
                'Instance',
                '102',
                "One of the sybase parameter is None so cannot proceed with instance creation")

        if self.has_instance(sybase_options["instance_name"]):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(
                    sybase_options["instance_name"])
            )

        if not self._commcell_object.storage_policies.has_policy(sybase_options["storage_policy"]):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    sybase_options["storage_policy"])
            )

        # encodes the plain text password using base64 encoding
        sa_password = b64encode(sybase_options["sa_password"].encode()).decode()
        localadmin_password = b64encode(sybase_options["localadmin_password"].encode()).decode()

        enable_auto_discovery = sybase_options["enable_auto_discovery"]

        request_json = {
            "instanceProperties": {
                "instance": {
                    "clientName": self._client_object.client_name,
                    "appName": "Sybase",
                    "instanceName": sybase_options["instance_name"],
                    "_type_": 5,
                    "applicationId": 5
                },
                "sybaseInstance": {
                    "sybaseOCS": sybase_options["sybase_ocs"],
                    "backupServer": sybase_options["backup_server"],
                    "sybaseHome": sybase_options["sybase_home"],
                    "sybaseASE": sybase_options["sybase_ase"],
                    "configFile": sybase_options["config_file"],
                    "enableAutoDiscovery": enable_auto_discovery,
                    "sharedMemoryDirectory": sybase_options["shared_memory_directory"],
                    "defaultDatabaseStoragePolicy": {
                        "storagePolicyName": sybase_options["storage_policy"]
                    },
                    "saUser": {"password": sa_password, "userName": sybase_options["sa_username"]},
                    "localAdministrator": {
                        "password": localadmin_password,
                        "userName": sybase_options["localadmin_username"]
                    }
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ADD_INSTANCE'], request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    instance_name = response.json(
                    )['response']['entity']['instanceName']
                    instance_id = response.json(
                    )['response']['entity']['instanceId']
                    agent_name = self._agent_object.agent_name
                    return self._instances_dict[agent_name](
                        self._agent_object, instance_name, instance_id
                    )

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_big_data_apps_instance(self, distributed_options):
        """
            Method to add big data apps instance to the given client.

            distributed_options {
                "instanceName": "ClusterInstance"
                "MasterNode" : $MASTER_NODE$ (Optional based on cluster Type. If not present set it to "")
                "dataAccessNodes": [
                    {
                        "clientName": "DataClient1"
                    }
                ]
            }

            Raises:
                SDKException:
                    if None value in Distributed options
                    if Big Data Apps instance with same name already exists
                    if cannot retrieve cluster type from default Instance
        """
        if None in distributed_options.values():
            raise SDKException(
                'Instance',
                '102',
                "One of the distributed parameter is None so cannot proceed with instance creation")

        if self.has_instance(distributed_options["instanceName"]):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(
                    distributed_options["instanceName"])
            )

        """
            Get Cluster Type from Default Instance to assign it to the New Instance.
            Atleast one instance should be present in the client.
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._INSTANCES)
        if flag:
            if response.json() and "instanceProperties" in response.json():
                clusterProperties = response.json()["instanceProperties"][0]
                clusterType = clusterProperties["distributedClusterInstance"]["clusterType"]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

        request_json = {
            "instanceProperties": {
                "instance": {
                    "clientId": int(self._client_object.client_id),
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": distributed_options["instanceName"],
                },
                "distributedClusterInstance": {
                    "clusterType": clusterType,
                    "instance": {
                        "instanceName": distributed_options["instanceName"]
                    },
                    "clusterConfig": {
                        "uxfsConfig": {
                            "coordinatorNode": {
                                "clientName": distributed_options["MasterNode"]
                            }
                        }
                    },
                    "dataAccessNodes": {
                        "dataAccessNodes": distributed_options["dataAccessNodes"]
                    }
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ADD_INSTANCE'], request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    instance_name = response.json(
                    )['response']['entity']['instanceName']
                    self.refresh()
                    return self.get(instance_name)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_s3_instance(self,
                        instance_name,
                        access_node,
                        storage_policy,
                        accesskey,
                        secretkey,
                        description=None,
                        number_of_streams=None):
        """ Method to add new S3 cloud apps instance to given client.

        Args :

            instance_name            (str)         --     name of the instance to be added

            access_node              (str)         --     name of the backup client to be
                associated with this instance

            storage_policy           (str)         --     name of the storage policy to be
                associated with this instance

            accesskey                (str)         --     access key of the account to be
                associated with this instance

            secretkey                (str)         --     secret key of the account to be
                associated with this instance

            description              (str)         --     description of this instance

            number_of_streams        (int)         --     number of data backup streams

        Returns :

            None

        Raises:
                SDKException:

                    if S3 instance with same name already exists

                    if given storage policy does not exists in commcell

        """

        if self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(instance_name)
            )
        if not self._commcell_object.storage_policies.has_policy(storage_policy):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(storage_policy)
            )

        request_json = {
            "instanceProperties": {
                "description": description,
                "instance": {
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": self._agent_object.agent_name,
                },
                "cloudAppsInstance": {
                    "instanceType": 5,
                    "s3Instance": {
                        "accessKeyId": accesskey,
                        "secretAccessKey": secretkey,
                        "hostURL": "s3.amazonaws.com"
                    },
                    "generalCloudProperties": {
                        "numberOfBackupStreams": number_of_streams,
                        "proxyServers": [
                            {
                                "clientName": access_node
                            }
                        ],
                        "storageDevice": {
                            "dataBackupStoragePolicy": {
                                "storagePolicyName": storage_policy
                            }
                        }
                    }
                }
            }
        }

        add_instance = self._commcell_object._services['ADD_INSTANCE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_instance, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']
                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    instance_name = response.json()['response']['entity']['instanceName']
                    instance_id = response.json()['response']['entity']['instanceId']
                    agent_name = self._agent_object.agent_name
                    return self._instances_dict[agent_name](
                        self._agent_object, instance_name, instance_id
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def add_azure_instance(self,
                           instance_name,
                           access_node,
                           storage_policy,
                           accountname,
                           accesskey,
                           description=None,
                           number_of_streams=None):
        """ Method to add new Azure cloud apps instance to given client.

        Args :

            instance_name            (str)         --     name of the instance to be added

            access_node              (str)         --     name of the backup client to be
                associated with this instance

            storage_policy           (str)         --     name of the storage policy to be
                associated with this instance

            accountname              (str)         --     name of the account to be
                associated with this instance

            accesskey                (str)         --     access key of the account to be
                associated with this instance

            description              (str)         --     description of this instance

            number_of_streams        (int)         --     number of data backup streams

        Returns :

            None

        Raises:
                SDKException:

                    if Azure instance with same name already exists

                    if given storage policy does not exists in commcell

        """
        if self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(instance_name)

            )

        if not self._commcell_object.storage_policies.has_policy(storage_policy):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(storage_policy)
            )

        request_json = {
            "instanceProperties": {
                "description": description,
                "instance": {
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": self._agent_object.agent_name,
                },
                "cloudAppsInstance": {
                    "instanceType": 6,

                    "generalCloudProperties": {
                        "numberOfBackupStreams": number_of_streams,
                        "proxyServers": [
                            {
                                "clientName": access_node
                            }
                        ],
                        "storageDevice": {
                            "dataBackupStoragePolicy": {
                                "storagePolicyName": storage_policy
                            }
                        }
                    },
                    "azureInstance": {
                        "accountName": accountname,
                        "accessKey": accesskey,
                        "hostURL": "blob.core.windows.net"
                    },
                }
            }
        }

        add_instance = self._commcell_object._services['ADD_INSTANCE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_instance, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    instance_name = response.json()['response']['entity']['instanceName']
                    instance_id = response.json()['response']['entity']['instanceId']
                    agent_name = self._agent_object.agent_name
                    return self._instances_dict[agent_name](
                        self._agent_object, instance_name, instance_id
                    )

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def add_oraclecloud_instance(self,
                                 instance_name,
                                 access_node,
                                 storage_policy,
                                 endpointurl,
                                 username,
                                 password,
                                 description=None,
                                 number_of_streams=None):
        """ Method to add new Oracle cloud apps instance to given client.

        Args :

            instance_name            (str)         --     name of the instance to be added

            access_node              (str)         --     name of the backup client to be
                associated with this instance

            storage_policy           (str)         --     name of the storage policy to be
                associated with this instance

            endpointurl              (str)         --     endpoint url of the account to
                be associated with this instance

            username                 (str)         --     username of the account to be
                associated with this instance

            password                 (str)         --     password of the account to be
                associated with this instance

            description              (str)         --     description of this instance

            number_of_streams        (int)         --     number of data backup streams

        Returns :

            None

        Raises:
                SDKException:

                    if oracle instance with same name already exists

                    if given storage policy does not exists in commcell

        """

        if self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(instance_name)

            )

        if not self._commcell_object.storage_policies.has_policy(storage_policy):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(storage_policy)
            )
        password = b64encode(password.encode()).decode()
        request_json = {
            "instanceProperties": {
                "description": description,
                "instance": {
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": self._agent_object.agent_name,
                },
                "cloudAppsInstance": {
                    "instanceType": 14,

                    "generalCloudProperties": {
                        "numberOfBackupStreams": number_of_streams,
                        "proxyServers": [
                            {
                                "clientName": access_node
                            }
                        ],
                        "storageDevice": {
                            "dataBackupStoragePolicy": {
                                "storagePolicyName": storage_policy
                            }
                        }
                    },
                    "oraCloudInstance": {
                        "endpointURL": endpointurl,
                        "user": {
                            "password": password,
                            "userName": username
                        }
                    }
                }
            }
        }

        add_instance = self._commcell_object._services['ADD_INSTANCE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_instance, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    instance_name = response.json()['response']['entity']['instanceName']
                    instance_id = response.json()['response']['entity']['instanceId']
                    agent_name = self._agent_object.agent_name
                    return self._instances_dict[agent_name](
                        self._agent_object, instance_name, instance_id
                    )

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def add_openstack_instance(self,
                               instance_name,
                               access_node,
                               storage_policy,
                               server_name,
                               username,
                               apikey,
                               description=None,
                               number_of_streams=None):
        """ Method to add new Openstack cloud apps instance to given client.

        Args :

            instance_name            (str)         --     name of the instance to be added

            access_node              (str)         --     name of the backup client to be
                associated with this instance

            storage_policy           (str)         --     name of the storage policy to be
                associated with this instance

            server_name              (str)         --     auth url or server name of the
                account to be associated with this instance

            username                 (str)         --     username of the account to be
                associated with this instance

            apikey                   (str)         --     API key of the account to be
                associated with this instance

            description              (str)         --     description of this instance

            number_of_streams        (int)         --     number of data backup streams

        Returns :

            None

        Raises:
                SDKException:

                    if openstack instance with same name already exists

                    if given storage policy does not exists in commcell

        """

        if self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(instance_name)

            )

        if not self._commcell_object.storage_policies.has_policy(storage_policy):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(storage_policy)
            )

        apikey = b64encode(apikey.encode()).decode()
        request_json = {
            "instanceProperties": {
                "description": description,
                "instance": {
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": self._agent_object.agent_name,
                },
                "cloudAppsInstance": {
                    "instanceType": 15,

                    "generalCloudProperties": {
                        "numberOfBackupStreams": number_of_streams,
                        "proxyServers": [
                            {
                                "clientName": access_node
                            }
                        ],
                        "storageDevice": {
                            "dataBackupStoragePolicy": {
                                "storagePolicyName": storage_policy
                            }
                        }
                    },
                    "openStackInstance": {
                        "serverName": server_name,
                        "credentials": {
                            "password": apikey,
                            "userName": username
                        }
                    }
                }
            }
        }

        add_instance = self._commcell_object._services['ADD_INSTANCE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_instance, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    instance_name = response.json()['response']['entity']['instanceName']
                    instance_id = response.json()['response']['entity']['instanceId']
                    agent_name = self._agent_object.agent_name
                    return self._instances_dict[agent_name](
                        self._agent_object, instance_name, instance_id
                    )

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def delete_cloud_apps_instance(self, instance_name):
        """ Deletes the instance from the cloud apps agent.

        Args :
            instance_name       (str)      --     name of the instance to be deleted

        Returns :
            None

        Raises :
            SDKException:

                    if the specified instance doesn't exist
                    if the agent type is other than cloud apps

        """
        if not self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" doesnot exist.'.format(instance_name)

            )

        if self._agent_object.agent_name != 'cloud apps':
            raise SDKException(
                'Instance',
                '102',
                'Delete cannot be performed on the instance of agent "{0}"'.format(
                    self._agent_object.agent_name)
            )
        if not isinstance(instance_name, basestring):
            raise SDKException('Instance', '101')
        else:
            instance_name = instance_name.lower()

        if self.has_instance(instance_name):
            delete_instance_service = self._commcell_object._services['INSTANCE'] % (
                self._instances[instance_name]
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', delete_instance_service
            )

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = response_value['errorString']

                        if error_message:
                            o_str = 'Failed to delete instance\nError: "{0}"'
                            raise SDKException('Instance', '102', o_str.format(error_message))
                        else:
                            if error_code == '0':
                                # initialize the backupsets again
                                # so the backupsets object has all the backupsets
                                self.refresh()
                            else:
                                o_str = ('Failed to delete instance with error code: "{0}"\n'
                                         'Please check the documentation for '
                                         'more details on the error').format(error_code)
                                raise SDKException('Instance', '102', o_str)
                    else:
                        error_code = response.json()['errorCode']
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to delete instance\nError: "{0}"'.format(error_message)
                        raise SDKException('Instance', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Instance', '102', 'No instance exists with name: "{0}"'.format(instance_name)
            )

    def refresh(self):
        """Refresh the instances associated with the Agent of the selected Client."""
        self._instances = self._get_instances()


class Instance(object):
    """Class for performing instance operations for a specific instance."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialise the instance object.

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class
        """
        self._agent_object = agent_object
        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        if instance_id:
            # Use the instance id provided in the arguments
            self._instance_id = str(instance_id)
        else:
            # Get the id associated with this instance
            self._instance_id = self._get_instance_id()

        self._INSTANCE = self._services['INSTANCE'] % (self._instance_id)
        self._RESTORE = self._services['RESTORE']

        self._properties = None
        self._restore_association = None

        self.backupsets = None
        self.subclients = None
        self.refresh()

    def _get_instance_id(self):
        """Gets the instance id associated with this backupset.

             Returns:
                str - id associated with this instance
        """
        instances = Instances(self._agent_object)
        return instances.get(self.instance_name).instance_id

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Instance class instance for Instance: "{0}" of Agent: "{1}"'
        return representation_string.format(
            self._instance["instanceName"], self._agent_object.agent_name
        )

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._INSTANCE)

        if flag:
            if response.json() and "instanceProperties" in response.json():
                self._properties = response.json()["instanceProperties"][0]

                self._instance = self._properties["instance"]
                self._instance_name = self._properties["instance"]["instanceName"].lower()
                self._instanceActivityControl = self._properties["instanceActivityControl"]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_instance_properties(self, attr_name, value):
        """sets the properties of this sub client.value is updated to instance once when post call
            succeeds.

            Args:
                attr_name   (str)   --  old value of the property. this should be instance variable

                value       (str)   --  new value of the property. this should be instance variable

            Raises:
                SDKException:
                    if failed to update number properties for subclient

        """
        try:
            backup = eval('self.%s' % attr_name)        # Take backup of old value
        except (AttributeError, KeyError):
            backup = None

        exec("self.%s = %s" % (attr_name, 'value'))     # set new value

        # _get_instance_properties_json method must be added in all child classes
        # not to be added for classes, which does not support updating properties
        request_json = self._get_instance_properties_json()

        flag, response = self._cvpysdk_object.make_request('POST', self._INSTANCE, request_json)

        output = self._process_update_response(flag, response)
        if output[0]:
            return
        else:
            o_str = 'Failed to update properties of subclient\nError: "{0}"'

            # Restore original value from backup on failure
            exec("self.%s = %s" % (attr_name, backup))
            raise SDKException('Subclient', '102', o_str.format(output[2]))

    def _process_update_response(self, flag, response):
        """Updates the subclient properties with the request provided.

            Args:
                update_request  (str)  --  update request specifying the details to update

            Returns:
                (bool, basestring, basestring):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if failed to update properties

                    if response is empty

                    if response is not success
        """
        if flag:
            if response.json():
                if "response" in response.json():
                    error_code = str(response.json()["response"][0]["errorCode"])

                    if error_code == "0":
                        return (True, "0", "")
                    else:
                        error_message = ""

                        if "errorString" in response.json()["response"][0]:
                            error_message = response.json()["response"][0]["errorString"]

                        if error_message:
                            return (False, error_code, error_message)
                        else:
                            return (False, error_code, "")
                elif "errorCode" in response.json():
                    error_code = str(response.json()['errorCode'])
                    error_message = response.json()['errorMessage']

                    if error_code == "0":
                        return (True, "0", "")

                    if error_message:
                        return (False, error_code, error_message)
                    else:
                        return (False, error_code, "")
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _process_restore_response(self, request_json):
        """Runs the CreateTask API with the request JSON provided for Restore,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if restore job failed

                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._RESTORE, request_json)

        self._restore_association = None

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedule(self._commcell_object, schedule_id=response.json()['taskId'])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _filter_paths(self, paths, is_single_path=False):
        """Filters the paths based on the Operating System, and Agent.

            Args:
                paths           (list)  --  list containing paths to be filtered

                is_single_path  (bool)  --  boolean specifying whether to return a single path
                                                or the entire list

            Returns:
                list    -   if the boolean is_single_path is set to False

                str     -   if the boolean is_single_path is set to True
        """
        for index, path in enumerate(paths):
            if int(self._agent_object.agent_id) == AppIDAType.WINDOWS_FILE_SYSTEM:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('/', '\\')
                else:
                    path = '\\'
            elif int(self._agent_object.agent_id) == AppIDAType.LINUX_FILE_SYSTEM:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('\\', '/')
                else:
                    path = '\\'
                path = '/' + path

            paths[index] = path

        if is_single_path:
            return paths[0]
        else:
            return paths

    def _restore_json(
            self,
            **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (list)  --  list of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API
        """

        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        if self._restore_association is None:
            self._restore_association = self._instance

        if restore_option.get('copy_precedence') is None:
            restore_option['copy_precedence'] = 0

        if restore_option.get('overwrite') is not None:
            restore_option['unconditional_overwrite'] = restore_option['overwrite']

        # restore_option should use client key for destination client info
        client = restore_option.get("client", self._agent_object._client_object)

        if isinstance(client, basestring):
            client = self._commcell_object.clients.get(client)

        restore_option["client_name"] = client.client_name
        restore_option["client_id"] = int(client.client_id)

        # set time zone
        from_time = restore_option.get("from_time", None)
        to_time = restore_option.get("to_time", None)
        time_list = ['01/01/1970 00:00:00', '1/1/1970 00:00:00']

        if from_time and from_time not in time_list:
            restore_option["from_time"] = from_time

        if to_time and to_time not in time_list:
            restore_option["to_time"] = to_time

        # set versions
        if "versions" in restore_option:
            versions = restore_option['versions']
            if not isinstance(versions, list):
                raise SDKException('Instance', '101')
            if 'win' in self._agent_object._client_object.os_info.lower():
                version_string = "|\\|#15!vErSiOnS|#15!\\{0}"
            else:
                version_string = "|/|#15!vErSiOnS|#15!/{0}"

            for version in versions:
                version = version_string.format(version)
                restore_option["paths"].append(version)

        self._restore_browse_option_json(restore_option)
        self._restore_common_options_json(restore_option)
        self._impersonation_json(restore_option)
        self._restore_destination_json(restore_option)
        self._restore_fileoption_json(restore_option)
        self._restore_volume_rst_option_json(restore_option)
        self._sync_restore_option_json(restore_option)

        request_json = {
            "taskInfo": {
                "associations": [self._restore_association],
                "task": self._json_task,
                "subTasks": [{
                    "subTaskOperation": 1,
                    "subTask": self._json_restore_subtask,
                    "options": {
                        "restoreOptions": {
                            "impersonation": self._impersonation_json_,
                            "browseOption": self._browse_restore_json,
                            "commonOptions": self._commonoption_restore_json,
                            "destination": self._destination_restore_json,
                            "fileOption": self._fileoption_restore_json,
                            "sharePointRstOption": self._restore_sharepoint_json,
                            "volumeRstOption": self._volume_restore_json
                        }
                    }
                }]
            }
        }

        if restore_option.get('schedule_pattern') is not None:
            request_json = SchedulePattern().create_schedule(request_json,
                                                             restore_option['schedule_pattern'])

        if "multinode_restore" in restore_option:

            self._destination_restore_json["destinationInstance"] = {
                "instanceName": restore_option.get('destination_instance', self.instance_name)
            }

            self._destination_restore_json["noOfStreams"] = restore_option.get('no_of_streams', 2)

            self._distributed_restore_json = {
                "distributedRestore": True,
                "dataAccessNodes": {
                    "dataAccessNodes": restore_option.get('data_access_nodes', [])
                },
                "isMultiNodeRestore": True,
                "backupConfiguration": {
                    "backupDataAccessNodes": restore_option.get('data_access_nodes', [])
                }
            }

            self._qr_restore_option = {
                "destAppTypeId": restore_option.get('destination_appTypeId', 64)
            }

            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["adminOpts"] = {
                "contentIndexingOption": {
                    "subClientBasedAnalytics": False
                }
            }

            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["destination"] = self._destination_restore_json
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["distributedAppsRestoreOptions"] = self._distributed_restore_json
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["qrOption"] = self._qr_restore_option

        if "sync_restore" in restore_option:
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["syncOption"] = self._sync_restore_json
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]["includeMetaData"] = True
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["destination"]["inPlace"] = True

        return request_json

    def _restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        preserve_level      : preserve level option to set in restore
                        proxy_client        : proxy that needed to be used for restore
                        impersonate_user    : Impersonate user options for restore
                        impersonate_password: Impersonate password option for restore
                                                in base64 encoded form
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up
                        validate_only       : To validate data backed up for restore


            Returns:
                object - instance of the Job class for this restore job if its an immediate Job
                         instance of the Schedule class for this restore job if its a scheduled Job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        if not (isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        paths = self._filter_paths(paths)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            restore_option=fs_options,
            schedule_pattern=schedule_pattern)

        return self._process_restore_response(request_json)

    def _restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                                                           the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                                                           files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        preserve_level      : preserve level option to set in restore
                        proxy_client        : proxy that needed to be used for restore
                        impersonate_user    : Impersonate user options for restore
                        impersonate_password: Impersonate password option for restore
                                                in base64 encoded form
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up
                        media_agent         : Media Agent need to be used for Browse and restore
                        validate_only       : To validate data backed up for restore


            Returns:
                object - instance of the Job class for this restore job if its an immediate Job
                         instance of the Schedule class for this restore job if its a scheduled Job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        from .client import Client

        if not ((isinstance(client, basestring) or isinstance(client, Client)) and
                isinstance(destination_path, basestring) and
                isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if fs_options is None:
            fs_options = {}

        if isinstance(client, Client):
            client = client
        elif isinstance(client, basestring):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        paths = self._filter_paths(paths)

        destination_path = self._filter_paths([destination_path], True)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            in_place=False,
            client=client,
            destination_path=destination_path,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            restore_option=fs_options,
            schedule_pattern=schedule_pattern
        )

        return self._process_restore_response(request_json)

    @property
    def _task(self):
        """Treats the task dict as read only property"""
        task = {
            "initiatedFrom": 2,
            "taskType": 1,
            "policyType": 0,
            "taskFlags": {
                "disabled": False
            }
        }

        return task

    @property
    def _restore_sub_task(self):
        """Treats the sub task dict as read only property"""
        sub_task = {
            "subTaskType": 3,
            "operationType": 1001
        }

        return sub_task

    @property
    def instance_id(self):
        """Treats the instance id as a read-only attribute."""
        return self._instance_id

    @property
    def instance_name(self):
        """Treats the instance name as a read-only attribute."""
        return self._instance_name

    def browse(self, *args, **kwargs):
        """Browses the content of the Instance.

            Args:
                Dictionary of browse options:
                    Example:

                        browse({
                            'path': 'c:\\\\hello',

                            'show_deleted': True,

                            'from_time': '2014-04-20 12:00:00',

                            'to_time': '2016-04-21 12:00:00'
                        })

            Kwargs:
                Keyword argument of browse options:
                    Example:

                        browse(
                            path='c:\\hello',

                            show_deleted=True,

                            from_time='2014-04-20 12:00:00',

                            to_time='2016-04-21 12:00:00'
                        )

            Returns:
                (list, dict)
                    list    -   List of only the file, folder paths from the browse response

                    dict    -   Dictionary of all the paths with additional metadata retrieved
                    from browse operation

            Raises:
                SDKException:
                    if there are more than one backupsets in the instance


            Refer `default_browse_options`_ for all the supported options.

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        # do browse operation if there is only one backupset in the instance
        # raise `SDKException` if there is more than one backupset in the instance

        if len(self.backupsets.all_backupsets) == 1:
            backupset_name = list(self.backupsets.all_backupsets.keys())[0]
            temp_backupset_obj = self.backupsets.get(backupset_name)
            return temp_backupset_obj.browse(*args, **kwargs)
        else:
            raise SDKException('Instance', '104')

    def find(self, *args, **kwargs):
        """Searches a file/folder in the backed up content of the instance,
            and returns all the files matching the filters given.

            Args:
                Dictionary of browse options:
                    Example:

                        find({
                            'file_name': '*.txt',

                            'show_deleted': True,

                            'from_time': '2014-04-20 12:00:00',

                            'to_time': '2016-04-31 12:00:00'
                        })

            Kwargs:
                Keyword argument of browse options:
                    Example:

                        find(
                            file_name='*.txt',

                            show_deleted=True,

                            'from_time': '2014-04-20 12:00:00',

                            to_time='2016-04-31 12:00:00'
                        )

            Returns:
                (list, dict)
                    list    -   List of only the file, folder paths from the browse response

                    dict    -   Dictionary of all the paths with additional metadata retrieved
                    from browse operation

            Raises:
                SDKException:
                    if there are more than one backupsets in the instance


            Refer `default_browse_options`_ for all the supported options.

            Additional options supported:
                file_name       (str)   --  Find files with name

                file_size_gt    (int)   --  Find files with size greater than size

                file_size_lt    (int)   --  Find files with size lesser than size

                file_size_et    (int)   --  Find files with size equal to size

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        # do find operation if there is only one backupset in the instance
        # raise `SDKException` if there is more than one backupset in the instance

        if len(self.backupsets.all_backupsets) == 1:
            backupset_name = list(self.backupsets.all_backupsets.keys())[0]
            temp_backupset_obj = self.backupsets.get(backupset_name)
            return temp_backupset_obj.find(*args, **kwargs)
        else:
            raise SDKException('Instance', '104')

    def _impersonation_json(self, value):
        """setter of Impersonation Json entity of Json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        use_impersonate = bool(value.get("impersonate_user"))

        self._impersonation_json_ = {
            "useImpersonation": use_impersonate,
            "user": {
                "userName": value.get("impersonate_user", ""),
                "password": value.get("impersonate_password", "")
            }
        }

    def _restore_browse_option_json(self, value):
        """setter  the Browse options for restore in Json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        if "copy_precedence" in value and value["copy_precedence"] != 0:
            value["copy_precedence_applicable"] = True

        time_range_dict = {}
        if value.get('from_time'):
            time_range_dict['fromTimeValue'] = value.get('from_time')

        if value.get('to_time'):
            time_range_dict['toTimeValue'] = value.get('to_time')

        self._browse_restore_json = {
            "listMedia": False,
            "useExactIndex": False,
            "noImage": value.get("no_image", False),
            "commCellId": 2,
            "mediaOption": {
                "mediaAgent": {
                    "mediaAgentName": value.get("media_agent", "")
                },
                "proxyForSnapClients": {
                    "clientName": value.get("proxy_client", '')
                },
                "library": {},
                "copyPrecedence": {
                    "copyPrecedenceApplicable": value.get("copy_precedence_applicable", False),
                    "copyPrecedence": value.get("copy_precedence", 0)
                },
                "drivePool": {}
            },
            "backupset": {
                "clientName": self._agent_object._client_object.client_name,
                "appName": self._agent_object.agent_name
            },
            "timeZone": {
                "TimeZoneName": "(UTC) Coordinated Universal Time",
            },
            "timeRange": time_range_dict
        }

        if "browse_job_id" in value:
            self._browse_restore_json["browseJobId"] = value.get("browse_job_id", False)
            self._browse_restore_json["browseJobCommCellId"] = value.get(
                "commcell_id", self._commcell_object.commcell_id)

    def _restore_common_options_json(self, value):
        """setter for  the Common options of in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "systemStateBackup": False,
            "clusterDBBackedup": False,
            "powerRestore": False,
            "restoreToDisk": False,
            "offlineMiningRestore": False,
            "onePassRestore": False,
            "detectRegularExpression": True,
            "wildCard": False,
            "preserveLevel": value.get("preserve_level", 1),
            "restoreToExchange": False,
            "stripLevel": 0,
            "restoreACLs": value.get("restore_ACL", True),
            "stripLevelType": value.get("striplevel_type", 0),
            "allVersion": value.get("all_versions", False),
            "unconditionalOverwrite": value.get("unconditional_overwrite", False),
            "includeAgedData": value.get("include_aged_data", False),
            "validateOnly": value.get("validate_only", False)
        }

        _advance_fs_keys = ["restoreDataInsteadOfStub",
                            "restoreOnlyStubExists",
                            "overwriteFiles",
                            "doNotOverwriteFileOnDisk",
                            "disableStubRestore"]

        if "fs_options" in value:
            _fs_option_value = value["fs_options"]
            if  _fs_option_value is not None:
                for _key in _advance_fs_keys:
                    if _key in _fs_option_value:
                        self._commonoption_restore_json[_key] = _fs_option_value[_key]

    def _restore_destination_json(self, value):
        """setter for  the destination restore option in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        # removed clientId from destClient as VSA Restores fail with it
        self._destination_restore_json = {
            "isLegalHold": False,
            "inPlace": value.get("in_place", True),
            "destPath": [value.get("destination_path", "")],
            "destClient": {
                "clientName": value.get("client_name", ""),
            }
        }

    def _restore_fileoption_json(self, value):
        """setter for  the fileoption restore option in restore JSON"""
        self._fileoption_restore_json = {
            "sourceItem": value.get("paths", []),
            "browseFilters": value.get("browse_filters", [])
        }

    def _restore_volume_rst_option_json(self, value):
        """setter for the volumeRst restore option in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._volume_restore_json = {
            "volumeLeveRestore": value.get("volume_level_restore", False),
            "volumeLevelRestoreType": value.get("volume_level_restore_type", "PHYSICAL_VOLUME")
        }

    def _sync_restore_option_json(self, value):
        """setter for the Sync. Restore option in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._sync_restore_json = {
            "PreserveModifiedFiles": True,
            "isMigration": True,
            "isSyncRestore": True,
            "paths": value.get("sync_option_paths")
        }

    @property
    def _restore_sharepoint_json(self):
        """getter for Sharepoint restore option in JSON. it is read only attribute"""
        _sharepoint_restore_json = {
            "is90OrUpgradedClient": False
        }

        return _sharepoint_restore_json

    @property
    def _json_task(self):
        """getter for the task information in JSON"""

        _taks_option_json = {
            "initiatedFrom": 2,
            "taskType": 1,
            "policyType": 0,
            "taskFlags": {
                "disabled": False
            }
        }

        return _taks_option_json

    @property
    def _json_restore_subtask(self):
        """getter for the subtask in restore JSON . It is read only attribute"""

        _subtask_restore_json = {
            "subTaskType": 3,
            "operationType": 1001
        }

        return _subtask_restore_json

    @property
    def _json_backup_subtasks(self):
        """getter for the subtask in restore JSON . It is read only attribute"""

        _backup_subtask = {
            "subTaskType": 2,
            "operationType": 2
        }

        return _backup_subtask

    def refresh(self):
        """Refresh the properties of the Instance."""
        from .backupset import Backupsets

        self._get_instance_properties()
        self.backupsets = Backupsets(self)
        self.subclients = Subclients(self)
