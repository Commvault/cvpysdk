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

    _process_add_response()         --  to process the add instance request using API call

    add_informix_instance()         --  adds new Informix Instance to given Client

    delete()                        --  deletes the instance specified by the instance_name
    from the agent.

    add_sybase_instance()           --  To add sybase server instance

    add_big_data_apps_instance()    --  To add an instance with the big data apps agent specified

    add_cloud_storage_instance()    --  Method to add a new cloud storage instance

    add_salesforce_instance()       --  Method to add a new salesforce instance

    add_postgresql_instance()       --  Method to add a new postgresql instance

    _set_general_properties_json()  --  setter for general cloud properties while adding a new
    cloud storage instance

    _set_instance_properties_json() --  setter for cloud storage instance properties while adding a
    new cloud storage instance

    refresh()                       --  refresh the instances associated with the agent
    
    add_mysql_instance()            --  Method to add new mysql Instance


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

    _restore_virtual_rst_option_json --  setter for the virtualServer restore option in restore JSON

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

    _process_update_request()       --  to process the request using API call

    _get_instance_properties_json() --  returns the instance properties

    update_properties()             --  to update the instance properties

    instance_id()                   --  id of this instance

    instance_name()                 --  name of this instance

    browse()                        --  browse the content of the instance

    find()                          --  find content in the instance

    refresh()                       --  refresh the properties of the instance

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

from base64 import b64encode
from past.builtins import basestring

from .job import Job
from .subclient import Subclients
from .constants import AppIDAType
from .exception import SDKException
from .schedules import SchedulePattern, Schedules


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

        self._general_properties = None
        self._instance_properties = None
        self._instances = None
        self._vs_instance_type_dict = {}
        self.refresh()

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
                    filter(lambda x: x[1] == value, self.all_instances.items())
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
        if 'file system' in self._agent_object.agent_name:
            return_dict = {
                'defaultinstancename': 1
            }
            return return_dict

        flag, response = self._cvpysdk_object.make_request('GET', self._INSTANCES)

        if flag:
            if response.json():
                if 'instanceProperties' in response.json():
                    return_dict = {}

                    instance_properties = response.json()['instanceProperties']
                    for dictionary in instance_properties:

                        agent = dictionary['instance']['appName'].lower()

                        if self._agent_object.agent_name in agent:
                            temp_name = dictionary['instance']['instanceName'].lower()
                            temp_id = str(dictionary['instance']['instanceId']).lower()
                            return_dict[temp_name] = temp_id

                        if 'vsInstanceType' in dictionary.get('virtualServerInstance', ''):
                            self._vs_instance_type_dict[str(dictionary['instance']['instanceId'])] = dictionary[
                                "virtualServerInstance"]["vsInstanceType"]

                    return return_dict
                elif 'errors' in response.json():
                    error = response.json()['errors'][0]
                    error_string = error['errorString']
                    raise SDKException('Instance', '102', error_string)
                else:
                    raise SDKException('Response', '102')
            else:
                return {}
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
                instance_name (str/int)  --  name or ID of the instance

            Returns:
                object - instance of the Instance class for the given instance name

            Raises:
                SDKException:
                    if type of the instance name argument is not string or Int

                    if no instance exists with the given name
        """
        if isinstance(instance_name, basestring):
            instance_name = instance_name.lower()

            if self.has_instance(instance_name):
                return Instance(self._agent_object, instance_name, self._instances[instance_name])

            raise SDKException(
                'Instance', '102', 'No instance exists with name: "{0}"'.format(instance_name)
            )
        elif isinstance(instance_name, int):
            instance_name = str(instance_name)
            instance_name = [name for name, instance_id in self.all_instances.items() if instance_name == instance_id]

            if instance_name:
                return self.get(instance_name[0])
            raise SDKException('Instance', '102', 'No Instance exists with the given ID: {0}'.format(instance_name))

        raise SDKException('Instance', '101')

    def _process_add_response(self, request_json):
        """Runs the Intance Add API with the request JSON provided,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                (bool, basestring, basestring):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._services['ADD_INSTANCE'], request_json)
        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to create instance\nError: "{0}"'.format(error_string)
                        raise SDKException('Instance', '102', o_str)
                    else:
                        # initialize the instances again
                        # so the instance object has all the instances
                        instance_name = response.json(
                        )['response']['entity']['instanceName']
                        self.refresh()
                        return self.get(instance_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create instance\nError: "{0}"'.format(error_string)
                    raise SDKException('Instance', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_informix_instance(self, informix_options):
        """Adds new Informix Instance to given Client
            Args:
                Dictionary of informix instance creation options:
                    Example:
                       informix_options = {
                            'instance_name': "",
                            'onconfig_file': "",
                            'sql_host_file': "",
                            'informix_dir': "",
                            'user_name': "",
                            'domain_name': "",
                            'password': "",
                            'storage_policy': "",
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
                            'instance_name': '',
                            'sybase_ocs': '',
                            'sybase_ase': '',
                            'backup_server': '',
                            'sybase_home': '',
                            'config_file': '',
                            'enable_auto_discovery': True,
                            'shared_memory_directory': '',
                            'storage_policy': '',
                            'sa_username': '',
                            'sa_password': '',
                            'localadmin_username': '',
                            'localadmin_password': ''
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

    def add_db2_instance(self, db2_options):
        """
            Method to Add new Db2 Instance to given Client
                Args:
                        Dictionary of db2 instance creation options:
                            Example:
                               db2_options = {
                                    'instance_name': 'db2inst1',
                                    'data_storage_policy': 'data_sp',
                                    'log_storage_policy': 'log_sp',
                                    'command_storage_policy': 'cmd_sp',
                                    'home_directory':'/home/db2inst1',
                                    'password':'db2inst1',
                                    'user_name':'db2inst1'
                                }
                    Raises:
                        SDKException:
                            if None value in db2 options

                            if db2 instance with same name already exists

                            if given storage policy does not exists in commcell

        """
        if not all(
                key in db2_options for key in(
                    "instance_name",
                    "data_storage_policy",
                    "log_storage_policy",
                    "command_storage_policy",
                    "home_directory",
                    "password",
                    "user_name")):
            raise SDKException(
                'Instance',
                '102',
                "Not all db2_options are provided")

        if not db2_options.get("instance_name"):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.')

        storage_policy = db2_options.get('storage_policy',db2_options.get('data_storage_policy'))

        if not self._commcell_object.storage_policies.has_policy(storage_policy):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    db2_options["data_storage_policy"])
            )

        # encodes the plain text password using base64 encoding

        #enable_auto_discovery = db2_options["enable_auto_discovery"]
        db2_password = b64encode(db2_options["password"].encode()).decode()

        request_json = {
            "instanceProperties": {
                "instance": {
                    "clientName": self._client_object.client_name,
                    "appName": "db2",
                    "instanceName": db2_options["instance_name"],
                },
                "db2Instance": {
                    "homeDirectory": db2_options["home_directory"],
                    "userAccount": {
                        "domainName": db2_options.get("domain_name", ''),
                        "password": db2_password,
                        "userName": db2_options["user_name"],
                    },

                    "DB2StorageDevice": {
                        "networkAgents": db2_options.get("network_agents", 1),
                        "softwareCompression": db2_options.get("software_compression", 0),
                        # "throttleNetworkBandwidth": db2_options.get("throttle_network_bandwidth", 500),
                        "dataBackupStoragePolicy": {
                            "storagePolicyName": storage_policy
                        },
                        "commandLineStoragePolicy": {
                            "storagePolicyName": storage_policy
                        },
                        "logBackupStoragePolicy": {
                            "storagePolicyName": storage_policy
                        },
                        "deDuplicationOptions": {
                            "generateSignature": db2_options.get("generate_signature", 1)
                        }
                    },
                    "overrideDataPathsForCmdPolicy":
                        db2_options.get("override_data_paths_for_cmd_policy", False)
                }
            }
        }
        add_instance = self._commcell_object._services['ADD_INSTANCE']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_instance, request_json)
        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'].get('errorCode')

                if error_code != 0:
                    error_string = response.json()['response'].get('errorString')
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating instance\nError: "{0}"'.format(error_string))
                else:
                    if 'entity' in response.json()['response']:
                        self.refresh()
                        return self._instances_dict[self._agent_object.agent_name](
                            self._agent_object,
                            response.json()['response']['entity'].get('instanceName'),
                            response.json()['response']['entity'].get('instanceId')
                        )
                    else:
                        raise SDKException('Instance', '102', 'Unable to get instance name and id'
                                           )
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

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
        cluster_properties = {}
        flag, response = self._cvpysdk_object.make_request('GET', self._INSTANCES)
        if flag:
            if response.json() and "instanceProperties" in response.json():
                cluster_properties = response.json()["instanceProperties"][0]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

        cluster_type = cluster_properties.get('distributedClusterInstance', {}).get('clusterType')
        cluster_config = {}
        uxfs_config = cluster_properties.get(
            'distributedClusterInstance', {}).get('clusterConfig', {}).get('uxfsConfig')
        hadoop_config = cluster_properties.get(
            'distributedClusterInstance', {}).get('clusterConfig', {}).get('hadoopConfig')
        if uxfs_config is not None:
            uxfs_config['coordinatorNode'] = {"clientName": distributed_options.get('MasterNode', '')}
            cluster_config['uxfsConfig'] = uxfs_config
        if hadoop_config is not None:
            hadoop_config['coordinatorNode'] = {"clientName": distributed_options.get('MasterNode', '')}
            hbase_config = hadoop_config.get('hadoopApps', {}).get('appConfigs', [{}])[0].get('hBaseConfig')
            if hbase_config is not None:
                hadoop_config["hadoopApps"]["appConfigs"][0]['hBaseConfig']["hbaseClientNode"] = {
                    "clientName": distributed_options.get('MasterNode', '')}
            cluster_config['hadoopConfig'] = hadoop_config

        request_json = {
            "instanceProperties": {
                "instance": {
                    "clientId": int(self._client_object.client_id),
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": distributed_options["instanceName"],
                },
                "distributedClusterInstance": {
                    "clusterType": cluster_type,
                    "instance": {
                        "instanceName": distributed_options["instanceName"]
                    },
                    "clusterConfig": cluster_config,
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

    def add_cloud_storage_instance(self, cloud_options):
        """Returns the JSON request to pass to the API for adding a cloud storage instance

        Args:
            cloud_options    (dict)    --    Options needed for adding a new cloud storage instance.

        Example:
        Cloud : S3
        cloud_options = {
                            'instance_name': 'S3',
                            'description': 'instance for s3',
                            'storage_policy':'cs_sp',
                            'number_of_streams': 2,
                            'access_node': 'CS',
                            'accesskey':'xxxxxxxx',
                            'secretkey':'yyyyyyyy',
                            'cloudapps_type': 's3'

            }
        Cloud : Google Cloud
        cloud_options = {
                            'instance_name': 'google_test',
                            'description': 'instance for google',
                            'storage_policy':'cs_sp',
                            'number_of_streams': 2,
                            'access_node': 'CS',
                            'cloudapps_type': 'google_cloud'
                            'host_url':'storage.googleapis.com',
                            'access_key':'xxxxxx',
                            'secret_key':'yyyyyy'
                        }
        Cloud : Azure Datalake Gen2
        cloud_options = {

                            'instance_name': 'TestAzureDL',
                            'access_node': 'CS',
                            'description': None,
                            'storage_policy': 'cs_sp',
                            'accountname': 'xxxxxx',
                            'accesskey': 'xxxxxx',
                            'number_of_streams': 1,
                            'cloudapps_type': 'azureDL'
                        }
        Cloud : Amazon RDS
        cloud_options = {
                            'instance_name': 'RDS',
                            'storage_plan': 'cs_sp',
                            'storage_policy': 'cs_sp',
                            'access_node': 'CS',
                            'access_key': 'xxxxx',
                            'secret_key': 'xxxxx',
                            'cloudapps_type': 'amazon_rds'
                        }
        Cloud : Amazon Redshift
        cloud_options = {

                            'instance_name': 'Redshift',
                            'storage_plan': 'cs_sp',
                            'storage_policy': 'cs_sp',
                            'access_node': 'CS',
                            'access_key': 'xxxxx',
                            'secret_key': 'xxxxx',
                            'cloudapps_type': 'amazon_redshift'
                        }
        Cloud : Amazon Document DB
        cloud_options = {
                            'instance_name': 'DocumentDB',
                            'storage_plan': 'cs_sp',
                            'storage_policy': 'cs_sp',
                            'access_node': 'CS',
                            'access_key': 'xxxxxx',
                            'secret_key': 'xxxxxx',
                            'cloudapps_type': 'amazon_docdb'
                        }
        Returns:
            dict     --   JSON request to pass to the API
        Raises :
            SDKException :

                if cloud storage instance with same name already exists

                if given storage policy does not exist in commcell

        Cloud : Amazon DynamoDB
        cloud_options = {
                            'instance_name': 'DynamoDB',
                            'storage_plan': 'cs_sp',
                            'storage_policy': 'cs_sp',
                            'access_node': 'CS',
                            'access_key': 'xxxxxx',
                            'secret_key': 'xxxxxx',
                            'cloudapps_type': 'amazon_dynamodb'
                        }
        Returns:
            dict     --   JSON request to pass to the API
        Raises :
            SDKException :

                if cloud storage instance with same name already exists

                if given storage policy does not exist in commcell

        """
        if cloud_options.get("instance_name"):
            if self.has_instance(cloud_options.get("instance_name")):
                raise SDKException(
                    'Instance', '102', 'Instance "{0}" already exists.'.format(
                        cloud_options.get("instance_name"))
                )
        else:
            raise SDKException(
                'Instance', '102', 'Empty instance name provided')

        if cloud_options.get("storage_policy"):
            if not self._commcell_object.storage_policies.has_policy(
                    cloud_options.get("storage_policy")):
                raise SDKException(
                    'Instance',
                    '102',
                    'Storage Policy: "{0}" does not exist in the Commcell'.format(
                        cloud_options.get("storage_policy"))
                )
        else:
            raise SDKException(
                'Instance', '102', 'Empty storage policy provided')
        if cloud_options.get('description'):
            description = cloud_options.get('description')
        else:
            description = ''

        self._instance_properties_json = cloud_options
        request_json = {
            "instanceProperties": {
                "description": description,
                "instance": {
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": cloud_options.get("instance_name"),
                    "appName": self._agent_object.agent_name,
                },
                "cloudAppsInstance": self._instance_properties_json
            }
        }

        if cloud_options.get("storage_plan"):
            request_json["instanceProperties"]["planEntity"] = {
                "planName": cloud_options.get("storage_plan")
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

    def add_salesforce_instance(
            self, instance_name, access_node,
            salesforce_options,
            db_options=None, **kwargs):
        """Adds a new salesforce instance.

            Args:
                instance_name               (str)   -- instance_name
                access_node                 (str)   -- access node name
                salesforce_options          (dict)  -- salesforce options
                                                        {
                                                                "login_url": 'salesforce login url',
                                                                "consume_id": 'salesforce consumer key',
                                                                "consumer_secret": 'salesforce consumer secret',
                                                                "salesforce_user_name": 'salesforce login user',
                                                                "salesforce_user_password": 'salesforce user password',
                                                                "salesforce_user_token": 'salesforce user token'
                                                        }

                db_options                  (dict)  -- database options to configure sync db
                                                        {
                                                            "db_enabled": 'True or False',
                                                            "db_type": 'SQLSERVER or POSTGRESQL',
                                                            "db_host_name": 'database hostname',
                                                            "db_instance": 'database instance name',
                                                            "db_name": 'database name',
                                                            "db_port": 'port of the database',
                                                            "db_user_name": 'database user name',
                                                            "db_user_password": 'database user password'
                                                        }

                **kwargs                    (dict)   -- dict of keyword arguments as follows

                                                         download_cache_path     (str)   -- download cache path
                                                         mutual_auth_path        (str)   -- mutual auth cert path
                                                         storage_policy          (str)   -- storage policy
                                                         streams                 (int)   -- number of streams
            Returns:
                object  -   instance of the instance class for this new instance

            Raises:
                SDKException:
                    if instance with given name already exists

                    if failed to add the instance

                    if response is empty

                    if response is not success
        """
        if db_options is None:
            db_options = {'db_enabled': False}
        if self.has_instance(instance_name):
            raise SDKException('Instance', '102',
                               'Instance "{0}" already exists.'.format(instance_name))

        salesforce_password = b64encode(salesforce_options.get('salesforce_user_password').encode()).decode()
        salesforce_consumer_secret = b64encode(
            salesforce_options.get('consumer_secret', '3951207263309722430').encode()).decode()
        salesforce_token = b64encode(salesforce_options.get('salesforce_user_token', '').encode()).decode()
        db_user_password = ""
        if db_options.get('db_enabled', False):
            db_user_password = b64encode(db_options.get('db_user_password').encode()).decode()

        request_json = {
            "instanceProperties": {
                "instance": {
                    "clientName": self._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": self._agent_object.agent_name
                },
                "cloudAppsInstance": {
                    "instanceType": 3,
                    "salesforceInstance": {
                        "enableREST": True,
                        "endpoint": salesforce_options.get('login_url', "https://login.salesforce.com"),
                        "consumerId": salesforce_options.get('consumer_id',
                                                             '3MVG9Nc1qcZ7BbZ0Ep18pfQsltTkZtbcMG9GMQzsVHGS8268yaOqmZ1lEEakAs8Xley85RBH1xKR1.eoUu1Z4'),
                        "consumerSecret": salesforce_consumer_secret,
                        "defaultBackupsetProp": {
                            "downloadCachePath": kwargs.get('download_cache_path', '/tmp'),
                            "mutualAuthPath": kwargs.get('mutual_auth_path', ''),
                            "token": salesforce_token,
                            "userPassword": {
                                "userName": salesforce_options.get('salesforce_user_name'),
                                "password": salesforce_password,
                            },
                            "syncDatabase": {
                                "dbEnabled": db_options.get('db_enabled', False),
                                "dbPort": db_options.get('db_port', "1433"),
                                "dbInstance": db_options.get('db_instance', ''),
                                "dbName": db_options.get('db_name', instance_name),
                                "dbType": db_options.get('db_type', 'SQLSERVER'),
                                "dbHost": db_options.get('db_host_name', ''),
                                "dbUserPassword": {
                                    "userName": db_options.get('db_user_name', ''),
                                    "password": db_user_password,

                                },
                            },
                        },
                    },
                    "generalCloudProperties": {
                        "numberOfBackupStreams": kwargs.get('streams', 2),
                        "proxyServers": [
                            {
                                "clientName": access_node
                            }
                        ],
                        "storageDevice": {
                            "dataBackupStoragePolicy": {
                                "storagePolicyName": kwargs.get('storage_policy', '')
                            },
                        },
                    },
                },
            },
        }
        self._process_add_response(request_json)

    def add_postgresql_instance(self, instance_name, **kwargs):
        """Adds new postgresql instance to given client
            Args:
                instance_name       (str)   --  instance_name
                kwargs              (dict)  --  dict of keyword arguments as follows:
                                                   storage_policy       (str)          -- storage policy
                                                   port                 (int or str)   -- port or end point
                                                   postgres_user_name   (str)          -- postgres user name
                                                   postgres_password    (str)          -- postgres password
                                                   version              (str)          -- postgres version
                                                   maintenance_db       (str)          -- maintenance db
                                                   binary_directory     (str)          -- postgres binary location
                                                   lib_directory        (str)          -- postgres lib location
                                                   archive_log_directory (str)         -- postgres archive log location
            Returns:
                object - instance of the Instance class

            Raises:
                SDKException:
                    if None value in mysql options

                    if mysql instance with same name already exists

                    if given storage policy does not exists in commcell
        """

        if self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(
                    instance_name)
            )
        password = b64encode(kwargs.get("postgres_password", "").encode()).decode()
        request_json = {
            "instanceProperties": {
                "instance": {
                    "clientName": self._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": "PostgreSQL",
                },
                "version": kwargs.get("version", "10.0"),
                "postGreSQLInstance": {
                    "LibDirectory": kwargs.get("lib_directory", ""),
                    "MaintainenceDB": kwargs.get("maintenance_db", "postgres"),
                    "port": kwargs.get("port", "5432"),
                    "ArchiveLogDirectory": kwargs.get("archive_log_directory", ""),
                    "BinaryDirectory": kwargs.get("binary_directory", ""),
                    "SAUser": {
                        "password": password,
                        "userName": kwargs.get("postgres_user_name", "postgres")
                    },
                    "logStoragePolicy": {
                        "storagePolicyName": kwargs.get("storage_policy", "")
                    },

                }
            }
        }
        self._process_add_response(request_json)


    @property
    def _general_properties_json(self):
        """Returns the general properties json."""
        return self._general_properties

    @_general_properties_json.setter
    def _general_properties_json(self, value):
        """setter for general cloud properties in instance JSON.

        Args:

            value    (dict)    --    options needed to set general cloud properties

        Example:

            value = {
                "number_of_streams":1,
                "access_node":"test",
                "storage_policy":"policy1",
                "access_key": "xxxxxx",
                "secret_key": "xxxxxx"
            }

        """

        supported_cloudapps_type = ["amazon_rds", "amazon_redshift",
                                    "amazon_docdb", "amazon_dynamodb"]
        if value.get("cloudapps_type") in supported_cloudapps_type:
            self._general_properties = {
                "accessNodes": {
                    "memberServers": [
                        {
                            "client": {
                                "clientName": value.get("access_node")
                            }
                        }
                    ]
                },
                "amazonInstanceInfo": {
                    "secretKey": value.get("secret_key"),
                    "accessKey": value.get("access_key")
                }
            }

        else:
            self._general_properties = {
                "numberOfBackupStreams": value.get("number_of_streams"),
                "proxyServers": [
                    {
                        "clientName": value.get("access_node")
                    }
                ],
                "storageDevice": {
                    "dataBackupStoragePolicy": {
                        "storagePolicyName": value.get("storage_policy")
                    }
                }
            }

    @property
    def _instance_properties_json(self):
        """Returns the instance properties json."""
        return self._instance_properties

    @_instance_properties_json.setter
    def _instance_properties_json(self, value):
        """setter for cloud storage instance properties in instance JSON.

        Args:

            value    (dict)    --    options needed to set cloud storage instance properties

        Example:
            value = {
                "accesskey" : "xxxxxxxxx"
                "secretkey" : "yyyyyyyy"
            }

        """

        supported_cloudapps_type = {"amazon_rds": 4, "amazon_redshift": 26,
                                    "amazon_docdb": 27, "amazon_dynamodb": 22}
        self._general_properties_json = value
        if value.get("cloudapps_type") == 's3':
            self._instance_properties = {
                "instanceType": 5,
                "s3Instance": {
                    "accessKeyId": value.get("accesskey"),
                    "secretAccessKey": value.get("secretkey"),
                    "hostURL": "s3.amazonaws.com"
                },
                "generalCloudProperties": self._general_properties_json
            }
        elif value.get("cloudapps_type") == 'azure':
            self._instance_properties = {
                "instanceType": 6,
                "azureInstance": {
                    "accountName": value.get("accountname"),
                    "accessKey": value.get("accesskey"),
                    "hostURL": "blob.core.windows.net"
                },
                "generalCloudProperties": self._general_properties_json
            }
        elif value.get("cloudapps_type") == 'oraclecloud':
            password = b64encode(value.get("password").encode()).decode()
            self._instance_properties = {
                "instanceType": 14,
                "oraCloudInstance": {
                    "endpointURL": value.get("endpointurl"),
                    "user": {
                        "password": password,
                        "userName": value.get("username")
                    }
                },
                "generalCloudProperties": self._general_properties_json
            }
        elif value.get("cloudapps_type") == 'openstack':
            apikey = b64encode(value.get("apikey").encode()).decode()
            self._instance_properties = {
                "instanceType": 15,
                "openStackInstance": {
                    "serverName": value.get("servername"),
                    "credentials": {
                        "password": apikey,
                        "userName": value.get("username")
                    }
                },
                "generalCloudProperties": self._general_properties_json
            }

        elif value.get("cloudapps_type") == 'google_cloud':
            secret_key = b64encode(value.get("secret_key").encode()).decode()
            self._instance_properties = {
                "instanceType": 20,
                "googleCloudInstance": {
                    "serverName": value.get("host_url"),
                    "credentials": {
                        "password": secret_key,
                        "userName": value.get("access_key")
                    }
                },
                "generalCloudProperties": self._general_properties_json
            }

        elif value.get("cloudapps_type") == 'azureDL':
            accesskey = b64encode(value.get("accesskey").encode()).decode()
            self._instance_properties = {
                "instanceType": 21,
                "azureDataLakeInstance": {
                    "serverName": "dfs.core.windows.net",
                    "credentials": {
                        "userName": value.get("accountname"),
                        "password": accesskey
                    }
                },
                "generalCloudProperties": self._general_properties_json
            }
        elif value.get("cloudapps_type") in supported_cloudapps_type:
            self._instance_properties = {
                "instanceType": supported_cloudapps_type[value.get("cloudapps_type")],
                "rdsInstance": {
                    "secretKey": value.get("secret_key"),
                    "accessKey": value.get("access_key"),
                    "regionEndPoints": "default"
                },
                "generalCloudProperties": self._general_properties_json
            }
    
    def add_mysql_instance(self, instance_name, database_options):
        """Adds new mysql Instance to given Client
            Args:
				instance_name       (str)   --  instance_name
              mysql_options       (dict)  --  dict of keyword arguments as follows:
                    Example:
                       database_options = {
                            'enable_auto_discovery': True,
                            'storage_policy': 'sai-sp',
                            'port': 'hotsname:port',
                            'mysql_user_name': 'mysqlusername'
                            'mysql_password': 'password',
                            'version': '5.7',
                            'binary_directory': "",
                            'config_file': "",
                            'log_data_directory': "",
                            'data_directory': "",
                            'description': "Automation created instance"
                        }

            Returns:
                object - instance of the Instance class

            Raises:
                SDKException:
                    if None value in mysql options

                    if mysql instance with same name already exists

                    if given storage policy does not exists in commcell
        """
        if None in database_options.values():
            raise SDKException(
                'Instance',
                '102',
                "One of the mysql parameter is None so cannot proceed with instance creation")

        if self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(
                    instance_name)
            )

        if not self._commcell_object.storage_policies.has_policy(
                database_options["storage_policy"]):
            raise SDKException(
                'Instance',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    database_options["storage_policy"])
            )
        password = b64encode(database_options["mysql_password"].encode()).decode()

        request_json = {
            "instanceProperties": {
                "description": "Automation created instance",
                "instance": {
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": "MySQL",
                    "applicationId": 104,
                    "_type_": 0
                },
                "mySqlInstance": {
                    "BinaryDirectory": database_options.get("binary_directory", ""),
                    "ConfigFile": database_options.get("config_file", ""),
                    "EnableAutoDiscovery": database_options.get("enable_auto_discovery", True),
                    "LogDataDirectory": database_options.get("log_data_directory", ""),
                    "dataDirectory": database_options.get("data_directory", ""),
                    "port": database_options.get("port", "3306"),
                    "version": database_options.get("version", "5.7"),
                    "sslCAFile": database_options.get("sslca_file_path", ""),
                    "SAUser": {
                        "password": password,
                        "userName": database_options.get("mysql_user_name", "mysql")
                    },
                    "mysqlStorageDevice": {
                        "commandLineStoragePolicy": {
                            "storagePolicyName": database_options.get("storage_policy", "")
                        },
                        "proxySettings": {
                            "isProxyEnabled": True,
                            "isUseSSL": True,
                            "runBackupOnProxy": True
                        }
                    }
                }
            }
        }
        self._process_add_response(request_json)

    def add_oracle_instance(self, instance_name, **oracle_options):
        """Adds new oracle instance for the given client
            Args:
                instance_name       (str)   --  instance_name (Oracle SID)
                oracle_options      (dict)  --  dict of keyword arguments as follows:
                                        log_storage_policy    (str)  -- log storage policy
                                        cmdline_storage_policy (str) -- Commandline data storage policy
                                        oracle_domain_name (str)   -- Domain name- only for windows
                                        oracle_user_name   (str)   -- oracle OS user name
                                        oracle_password    (str)   -- oracle OS user password
                                        oracle_home        (str)   -- oracle home path
                                        tns_admin          (str)   -- tns admin path
                                        connect_string     (dict)  -- Credentials to connect to Oracle DB
                                        {
                                            "username": "", (str)         -- User to connect to Oracle DB
                                            "password": "", (str)         -- Password
                                            "service_name": ""  (str)     -- Oracle SID or service name
                                        }
                                        catalog_connect     (dict)--  Credentials to connect to catalog
                                        {
                                            "userName": "",  (str)        -- Catalog DB user name
                                            "password"; "",  (str)        -- Password of catalog user
                                            "domainName": ""    (str)     -- SID of catalog database
                                        }
            Returns:
                object - instance of the Instance class
            Raises:
                SDKException:
                            if instance with same name exists already
                            if required options are not provided
                            Given storage policies do not exist in Commcell
        """

        if self.has_instance(instance_name):
            raise SDKException(
                'Instance', '102', 'Instance "{0}" already exists.'.format(
                    instance_name)
            )
        required_options = ['oracle_user_name', 'oracle_home', 'cmdline_storage_policy',
                            'log_storage_policy', 'connect_string']
        for option in required_options:
            if option not in oracle_options.keys():
                raise SDKException(
                    'Instance',
                    '102',
                    "Required option: {0} is missing, Please provide all parameters:".format(option))
        password = b64encode(oracle_options.get("oracle_password", "").encode()).decode()
        connect_string_password = b64encode(
            oracle_options.get("connect_string", {}).get("password", "").encode()
        ).decode()

        request_json = {
            "instanceProperties": {
                "instance": {
                    "clientName": self._client_object.client_name,
                    "instanceName": instance_name,
                    "appName": "Oracle",
                },
                "oracleInstance": {
                    "TNSAdminPath": oracle_options.get("tns_admin", ""),
                    "oracleHome": oracle_options.get("oracle_home", ""),
                    "oracleUser": {
                        "userName": oracle_options.get("oracle_user_name", ""),
                        "domainName": oracle_options.get("oracle_domain_name", ""),
                        "password": password,
                    },
                    "sqlConnect": {
                        "domainName": oracle_options.get("connect_string", {}).get("service_name", ""),
                        "userName": oracle_options.get("connect_string", {}).get("username", "/"),
                        "password": connect_string_password,
                    },
                    "oracleStorageDevice": {
                        "commandLineStoragePolicy": {
                            "storagePolicyName": oracle_options.get("cmdline_storage_policy", "")
                        },
                        "logBackupStoragePolicy": {
                            "storagePolicyName": oracle_options.get("log_storage_policy", "")
                        }
                    },
                }
            }
        }
        if oracle_options.get("catalog_connect"):
            catalog = {
                'useCatalogConnect': True,
                'catalogConnect': oracle_options.get("catalog_connect", "")
            }
            request_json['instanceProperties']['oracleInstance'].update(catalog)
        self._process_add_response(request_json)

    def refresh(self):
        """Refresh the instances associated with the Agent of the selected Client."""
        self._instances = self._get_instances()


class Instance(object):
    """Class for performing instance operations for a specific instance."""

    def __new__(cls, agent_object, instance_name, instance_id=None):
        from .instances.vsinstance import VirtualServerInstance
        from .instances.cainstance import CloudAppsInstance
        from .instances.bigdataappsinstance import BigDataAppsInstance
        from .instances.sqlinstance import SQLServerInstance
        from .instances.hanainstance import SAPHANAInstance
        from .instances.oracleinstance import OracleInstance
        from .instances.sybaseinstance import SybaseInstance
        from .instances.saporacleinstance import SAPOracleInstance
        from .instances.mysqlinstance import MYSQLInstance
        from .instances.lotusnotes.lndbinstance import LNDBInstance
        from .instances.lotusnotes.lndocinstance import LNDOCInstance
        from .instances.lotusnotes.lndminstance import LNDMInstance
        from .instances.postgresinstance import PostgreSQLInstance
        from .instances.informixinstance import InformixInstance
        from .instances.vminstance import VMInstance
        from .instances.db2instance import DB2Instance
        from .instances.aadinstance import AzureAdInstance
        from .instances.sharepointinstance import SharepointInstance

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        _instances_dict = {
            'virtual server': [VirtualServerInstance, VMInstance],
            'big data apps': BigDataAppsInstance,
            'cloud apps': CloudAppsInstance,
            'sql server': SQLServerInstance,
            'sap hana': SAPHANAInstance,
            'oracle': OracleInstance,
            'oracle rac': OracleInstance,
            'sybase': SybaseInstance,
            'sap for oracle': SAPOracleInstance,
            'mysql': MYSQLInstance,
            'notes database': LNDBInstance,
            'notes document': LNDOCInstance,
            'domino mailbox archiver': LNDMInstance,
            'postgresql': PostgreSQLInstance,
            'informix': InformixInstance,
            'db2': DB2Instance,
            'azure ad': AzureAdInstance,
            'sharepoint server': SharepointInstance
        }
        agent_name = agent_object.agent_name

        if agent_name in _instances_dict:
            if isinstance(_instances_dict[agent_name], list):
                if instance_name == "vminstance":
                    _class = _instances_dict[agent_name][-1]
                else:
                    _class = _instances_dict[agent_name][0]
            else:
                _class = _instances_dict[agent_name]
            if _class.__new__ == cls.__new__:
                return object.__new__(_class)
            return _class.__new__(_class, agent_object, instance_name, instance_id)
        else:
            return object.__new__(cls)

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
        self._instance_name = instance_name.lower()

        if instance_id:
            # Use the instance id provided in the arguments
            self._instance_id = str(instance_id)
        else:
            # Get the id associated with this instance
            self._instance_id = self._get_instance_id()

        self._INSTANCE = self._services['INSTANCE'] % (self._instance_id)
        self._ALLINSTANCES = self._services['GET_ALL_INSTANCES'] % (
            self._agent_object._client_object.client_id
        )
        self._RESTORE = self._services['RESTORE']

        self._properties = None
        self._restore_association = None

        # Restore json instance var
        self._commonopts_restore_json = {}

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
        # skip GET instance properties api call if instance id is 1
        if int(self.instance_id) == 1:
            self._properties = {
                'instance': {
                    "clientId": int(self._agent_object._client_object.client_id),
                    "clientName": self._agent_object._client_object.client_name,
                    "instanceName": self.instance_name,
                    "appName": self._agent_object.agent_name,
                    "instanceId": int(self.instance_id),
                    "applicationId": int(self._agent_object.agent_id)
                }
            }

            self._instance = self._properties["instance"]
            # stop the execution here for instance id 1 (DefaultInstanceName)
            return

        instance_service = (
            "{0}?association/entity/clientId={1}&association/entity/applicationId={2}".format(
                self._INSTANCE, self._agent_object._client_object.client_id,
                self._agent_object.agent_id
            )
        )
        flag, response = self._cvpysdk_object.make_request('GET', instance_service)

        if flag:
            if response.json() and "instanceProperties" in response.json():
                self._properties = response.json()["instanceProperties"][0]
                try:
                    self._instance = self._properties["instance"]
                    self._instance_name = self._properties["instance"]["instanceName"].lower()
                    self._instanceActivityControl = self._properties["instanceActivityControl"]
                except KeyError:
                    instance_service = (
                        "{0}&applicationId={1}".format(self._ALLINSTANCES, self._agent_object.agent_id))
                    flag, response = self._cvpysdk_object.make_request('GET', instance_service)
                    if flag:
                        if response.json() and "instanceProperties" in response.json():
                            self._properties = response.json()["instanceProperties"][0]
                            self._instance = self._properties["instance"]
                            self._instance_name = self._properties["instance"]["instanceName"].lower()
                            self._instanceActivityControl = self._properties["instanceActivityControl"]
                    else:
                        raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_instance_properties_json(self):
        """get the all instance related properties.

           Returns:
                dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties": {
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl
            }
        }

        return instance_json

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
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

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

        if restore_option.get('live_browse'):
            restore_option['liveBrowse'] = True
        else:
            restore_option['liveBrowse'] = False
        
        if restore_option.get('file_browse'):
            restore_option['fileBrowse'] = True
        else:
            restore_option['fileBrowse'] = False

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
        self._restore_virtual_rst_option_json(restore_option)
        self._restore_volume_rst_option_json(restore_option)
        self._sync_restore_option_json(restore_option)
        self._restore_common_opts_json(restore_option)

        if not restore_option.get('index_free_restore', False):
            if restore_option.get("paths") == []:
                raise SDKException('Subclient', '104')

        request_json = {
            "taskInfo": {
                "associations": [self._restore_association],
                "task": self._json_task,
                "subTasks": [{
                    "subTaskOperation": 1,
                    "options": {
                        "restoreOptions": {
                            "impersonation": self._impersonation_json_,
                            "browseOption": self._browse_restore_json,
                            "commonOptions": self._commonoption_restore_json,
                            "destination": self._destination_restore_json,
                            "fileOption": self._fileoption_restore_json,
                            "virtualServerRstOption": self._virtualserver_restore_json,
                            "sharePointRstOption": self._restore_sharepoint_json,
                            "volumeRstOption": self._volume_restore_json
                        },
                        "commonOpts": self._commonopts_restore_json
                    }
                }]
            }
        }

        if restore_option.get('index_free_restore', False):
            request_json["taskInfo"]["subTasks"][0]["subTask"] = self._json_restore_by_job_subtask
            jobs_list = restore_option.get('restore_jobs')
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["jobIds"] = jobs_list
            source_item = []
            for i in jobs_list:
                source_item.append("2:{0}".format(i))
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"]["sourceItem"] = source_item

        else:
            request_json["taskInfo"]["subTasks"][0]["subTask"] = self._json_restore_subtask

        if restore_option.get('schedule_pattern') is not None:
            request_json = SchedulePattern().create_schedule(request_json,
                                                             restore_option['schedule_pattern'])

        if restore_option.get("multinode_restore", False):

            self._distributed_restore_json = {
                "clientType": restore_option.get('client_type', 0),
                "distributedRestore": restore_option.get("multinode_restore", False),
                "dataAccessNodes": {
                    "dataAccessNodes": restore_option.get('data_access_nodes', [])
                },
                "isMultiNodeRestore": restore_option.get("multinode_restore", False),
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

            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["distributedAppsRestoreOptions"] = self._distributed_restore_json
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["qrOption"] = self._qr_restore_option

        if restore_option.get("destination_appTypeId", False):
            self._qr_restore_option = {
                "destAppTypeId": restore_option.get('destination_appTypeId')
            }
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "qrOption"] = self._qr_restore_option

        if "sync_restore" in restore_option:
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["syncOption"] = self._sync_restore_json
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]["includeMetaData"] = True
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["destination"]["inPlace"] = True

        if 'backup_level' in restore_option:
            backup_opt_json = {
                "backupLevel": restore_option.get('backup_level', 'Incremental')
            }
            request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"] = backup_opt_json

        if restore_option.get('restore_acls_only', False):
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["restoreACLsType"] = 1

        if restore_option.get('restore_data_only', False):
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["restoreACLsType"] = 2

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
            schedule_pattern=None,
            proxy_client=None,
            restore_jobs=[],
            advanced_options=None
    ):
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

                        no_of_streams   (int)       -- Number of streams to be used for restore

                proxy_client    (str)          -- Proxy client used during FS under NAS operations

                restore_jobs    (list)          --  list of jobs to be restored if the job is index free restore

                advanced_options    (dict)  -- Advanced restore options

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

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

        request_json = self._restore_json(
            paths=paths,
            in_place=True,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            restore_option=fs_options,
            schedule_pattern=schedule_pattern,
            proxy_client=proxy_client,
            restore_jobs=restore_jobs,
            advanced_options=advanced_options
        )

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
            schedule_pattern=None,
            proxy_client=None,
            restore_jobs=[],
            advanced_options=None,
    ):
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

                        no_of_streams   (int)       -- Number of streams to be used for restore

                proxy_client    (str)          -- Proxy client used during FS under NAS operations

                restore_jobs    (list)          --  list of jobs to be restored if the job is index free restore

                advanced_options    (dict)  -- Advanced restore options

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

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
            schedule_pattern=schedule_pattern,
            proxy_client=proxy_client,
            restore_jobs=restore_jobs,
            advanced_options=advanced_options
        )

        return self._process_restore_response(request_json)

    def _process_update_request(self, request_json):
        """Runs the Instance update API

            Args:
                request_json    (dict)  -- request json sent as payload

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._INSTANCE, request_json
        )

        status, _, error_string = self._process_update_response(flag, response)

        if not status:
            raise SDKException('Instance', '102', 'Failed to update the instance properties\nError: "{0}"'.format(
                error_string))
        self.refresh()

    def update_properties(self, properties_dict):
        """Updates the instance properties

            Args:
                properties_dict (dict)  --  instance properties dict which is to be updated

            Returns:
                None

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected

        **Note** self.properties can be used to get a deep copy of all the properties, modify the properties which you
        need to change and use the update_properties method to set the properties

        """
        request_json = {
            "instanceProperties": {

            }
        }

        request_json['instanceProperties'].update(properties_dict)
        self._process_update_request(request_json)

    @property
    def properties(self):
        """Returns the instance properties"""
        return copy.deepcopy(self._properties)

    @property
    def name(self):
        """Returns the Instance Display name"""
        return self._properties["instance"]["instanceName"]

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
        options = value.get("advanced_options") or {}

        if value.get('from_time'):
            time_range_dict['fromTimeValue'] = value.get('from_time')

        if value.get('to_time'):
            time_range_dict['toTimeValue'] = value.get('to_time')

        self._browse_restore_json = {
            "listMedia": False,
            "useExactIndex": False,
            "noImage": value.get("no_image", False),
            "commCellId": 2,
            "liveBrowse": value.get('live_browse', False),
            "mediaOption": {
                "mediaAgent": {
                    "mediaAgentName": value.get("media_agent", None) or ""
                },
                "proxyForSnapClients": {
                    "clientName": value.get("snap_proxy", None) or value.get("proxy_client", None) or ""
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
                "TimeZoneName": options.get("timezone", self._commcell_object.default_timezone)
            },
            "timeRange": time_range_dict
        }

        if "browse_job_id" in value:
            self._browse_restore_json["browseJobId"] = value.get("browse_job_id", False)
            self._browse_restore_json["browseJobCommCellId"] = value.get(
                "commcell_id", self._commcell_object.commcell_id)

        if value.get('iscsi_server'):

            self._browse_restore_json['mediaOption']['iSCSIServer'] = {
                'clientName': value.get("iscsi_server")
            }

        # Add this option to enable restoring of troubleshooting folder
        if value.get("include_metadata", False):
            self._browse_restore_json["includeMetaData"] = True

    def _restore_common_opts_json(self, value):
        """ Method to set commonOpts for restore

        Args:
             value  (dict)  -- restore options dictionary

        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        options = value.get("advanced_options")

        if not options:
            return

        # taskInfo -> subTasks -> options -> commonOpts
        self._commonopts_restore_json = {
            "jobDescription": options.get("job_description", "")
        }

    def _restore_common_options_json(self, value):
        """setter for  the Common options of in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "systemStateBackup": False,
            "clusterDBBackedup": False,
            "powerRestore": False,
            "restoreToDisk": value.get("restore_to_disk", False),
            "indexFreeRestore": value.get("index_free_restore", False),
            "offlineMiningRestore": False,
            "onePassRestore": False,
            "detectRegularExpression": True,
            "wildCard": False,
            "preserveLevel": value.get("preserve_level", 1),
            "restoreToExchange": False,
            "stripLevel": 0,
            "restoreACLs": value.get("restore_ACL", value.get("restore_data_and_acl", True)),
            "stripLevelType": value.get("striplevel_type", 0),
            "allVersion": value.get("all_versions", False),
            "unconditionalOverwrite": value.get("unconditional_overwrite", False),
            "includeAgedData": value.get("include_aged_data", False),
            "validateOnly": value.get("validate_only", False)
        }

        if value.get("instant_clone_options", {}).get("post_clone_script", None):
            self._commonoption_restore_json['prePostCloneOption'] = {
                'postCloneCmd': value.get("instant_clone_options").get("post_clone_script")
            }

        _advance_fs_keys = ["restoreDataInsteadOfStub",
                            "restoreOnlyStubExists",
                            "overwriteFiles",
                            "doNotOverwriteFileOnDisk",
                            "disableStubRestore"]

        if "fs_options" in value:
            _fs_option_value = value["fs_options"]
            if _fs_option_value is not None:
                for _key in _advance_fs_keys:
                    if _key in _fs_option_value:
                        self._commonoption_restore_json[_key] = _fs_option_value[_key]

    def _restore_destination_json(self, value):
        """setter for  the destination restore option in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        if value.get("proxy_client") is not None and \
                (self._agent_object.agent_name).upper() == "FILE SYSTEM":
            self._destination_restore_json = {
                "inPlace": value.get("in_place", True),
                "destClient": {
                    "clientName": value.get("proxy_client", "")
                }
            }
            if value.get('destination_path'):
                destination_path = value.get("destination_path", "")
                self._destination_restore_json["destPath"] = [destination_path] if destination_path != "" else []

        # For Index server restore, we need to set proxy client & in-place flag
        elif value.get("proxy_client") is not None and \
                (self._agent_object.agent_name).upper() == "BIG DATA APPS" and \
                self.name.upper() == "DYNAMICINDEXINSTANCE":
            self._destination_restore_json = {
                "inPlace": value.get("in_place", True),
                "destClient": {
                    "clientName": value.get("proxy_client", "")
                }
            }
        else:
            # removed clientId from destClient as VSA Restores fail with it
            self._destination_restore_json = {
                "isLegalHold": False,
                "inPlace": value.get("in_place", True),
                "destPath": [value.get("destination_path", "")],
                "destClient": {
                    "clientName": value.get("client_name", ""),
                }
            }
            # removing 'destPath' if restoring in place
            self._destination_restore_json.pop('destPath') if value.get("in_place", True) else None

        if value.get("multinode_restore", False) or value.get("no_of_streams", 1) > 1:
            self._destination_restore_json["destinationInstance"] = {
                "instanceName": value.get('destination_instance', self.instance_name)
            }
            if value.get('destination_instance_id') is not None:
                self._destination_restore_json["destinationInstance"]["instanceId"] = int(
                    value.get('destination_instance_id')
                    )

            self._destination_restore_json["noOfStreams"] = value.get('no_of_streams', 2)

    def _restore_fileoption_json(self, value):
        """setter for  the fileoption restore option in restore JSON"""
        self._fileoption_restore_json = {
            "sourceItem": value["instant_clone_options"]["instant_clone_src_path"] if value.get("instant_clone_options", None) else value.get("paths", []),
            "browseFilters": value.get("browse_filters", [])
        }

        if value.get("instant_clone_options", None):
            self._fileoption_restore_json["fsCloneOptions"] = {
                "reservationTime": value["instant_clone_options"]["reservation_time"],
                "cloneMountPath": value["instant_clone_options"]["clone_mount_path"]}

            if value["instant_clone_options"].get("clone_cleanup_script", None):
                self._fileoption_restore_json["fsCloneOptions"]["cloneCleanupOptions"] = {
                    "cleanupScriptPath": value.get("instant_clone_options").get("clone_cleanup_script")
                }

    def _restore_virtual_rst_option_json(self, value):
        """setter for the virtualServer restore option in restore JSON"""
        self._virtualserver_restore_json = {
            "isFileBrowse": value.get("fileBrowse")
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
    def _json_restore_by_job_subtask(self):
        """getter for the subtast in restore by job JSON"""

        _subtask_restore_by_job_json = {
            "subTaskType": 3,
            "operationType": 1005
        }

        return _subtask_restore_by_job_json

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
