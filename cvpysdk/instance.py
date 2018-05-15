#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing instance operations.

Instances and Instance are 2 classes defined in this file.

Instances: Class for representing all the instances associated with a specific agent

Instance:  Class for a single instance selected for an agent,
                and to perform operations on that instance


Instances:
    __init__(agent_object)          --  initialise object of Instances class associated with
                                            the specified agent

    __str__()                       --  returns all the instances associated with the agent

    __repr__()                      --  returns the string for the object of the Instances class

    _get_instances()                --  gets all the instances associated with the agent specified

    has_instance(instance_name)     --  checks if a instance exists with the given name or not

    get(instance_name)              --  returns the Instance class object
                                            of the input backup set name


Instance:
    __init__(agent_object,
             instance_name,
             instance_id=None)      --  initialise object of Instance with the specified instance
                                             name and id, and associated to the specified agent

    __repr__()                      --  return the instance name, the object is associated with

    _get_instance_id()              --  method to get the instance id, if not specified in __init__

    _get_instance_properties()      --  method to get the properties of the instance

    _process_update_response()      --  updates the instance properties

    _process_restore_response()     --  processes the restore request sent to server
                                            and returns the restore job object

    _filter_paths()                 --  filters the path as per the OS, and the Agent

    _restore_json()                 --  returns the apppropriate JSON request to pass for either
                                            Restore In-Place or Out-of-Place operation

    _restore_in_place()             --  Restores the files/folders specified in the
                                            input paths list to the same location

    _restore_out_of_place()         --  Restores the files/folders specified in the input paths
                                            list to the input client, at the specified destionation
                                            location

    _task()                         --  the task dict used while restore/backup job

    _restore_sub_task()             --  the restore job specific sub task dict used to form
                                            restore json

    instance_id()                   --  id of this instance

    instance_name()                 --  name of this instance

    browse()                        --  browse the content of the instance

    find()                          --  find content in the instance

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

from .job import Job
from .subclient import Subclients
from .constants import AppIDAType
from .exception import SDKException


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
        self._commcell_object = self._agent_object._commcell_object

        self._INSTANCES = self._commcell_object._services['GET_ALL_INSTANCES'] % (
            self._agent_object._client_object.client_id
        )

        self._instances = self._get_instances()

        from .instances.vsinstance import VirtualServerInstance
        from .instances.cainstance import CloudAppsInstance
        from .instances.sqlinstance import SQLServerInstance
        from .instances.hanainstance import SAPHANAInstance
        from .instances.oracleinstance import OracleInstance

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        self._instances_dict = {
            'virtual server': VirtualServerInstance,
            'cloud apps': CloudAppsInstance,
            'sql server': SQLServerInstance,
            'sap hana': SAPHANAInstance,
            'oracle': OracleInstance
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
                self._agent_object._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Instances class."""
        return "Instances class instance for Agent: '{0}'".format(self._agent_object.agent_name)

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._INSTANCES)

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
        from .backupset import Backupsets

        self._agent_object = agent_object
        self._commcell_object = self._agent_object._commcell_object

        if instance_id:
            # Use the instance id provided in the arguments
            self._instance_id = str(instance_id)
        else:
            # Get the id associated with this instance
            self._instance_id = self._get_instance_id()

        self._INSTANCE = self._commcell_object._services['INSTANCE'] % (self._instance_id)
        self._RESTORE = self._commcell_object._services['RESTORE']
        self._properties = None
        self._restore_association = None

        self._get_instance_properties()

        self.backupsets = Backupsets(self)
        self.subclients = Subclients(self)

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._INSTANCE)

        if flag:
            if response.json() and "instanceProperties" in response.json():
                self._properties = response.json()["instanceProperties"][0]

                self._instance = self._properties["instance"]
                self._instance_name = self._properties["instance"]["instanceName"].lower()
                self._instanceActivityControl = self._properties["instanceActivityControl"]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _set_instance_properties(self, attr_name, value):
        """sets the properties of this sub client.value is updated to instance once when post call
            succeeds

            Args:
                attr_name (str)  --  old value of the property. this should be instance variable.
                value (str)  --  new value of the property. this should be instance variable.

            Raises:
                SDKException:
                    if failed to update number properties for subclient


        """
        backup = None
        exec("backup = self.%s" % (attr_name))          #Take backup of old value
        exec("self.%s = %s" % (attr_name, 'value'))       #set new value

        request_json = self._get_instance_properties_json()
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._INSTANCE, request_json
        )

        output = self._process_update_response(flag, response)
        if output[0]:
            return
        else:
            o_str = 'Failed to update properties of subclient\nError: "{0}"'
            exec("self.%s = %s" % (attr_name, backup)) # Restore original value from backup on failure
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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._RESTORE, request_json
        )

        self._restore_association = None

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
            paths,
            in_place=True,
            client=None,
            destination_path=None,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                paths   (list)  --  list of full paths of files/folders to restore

            Returns:
                dict - JSON request to pass to the API
        """
        if self._restore_association is None:
            self._restore_association = self._instance

        if client is None and destination_path is None:
            client_id = int(self._agent_object._client_object.client_id)
            client_name = self._agent_object._client_object.client_name
        else:
            client_id = int(client.client_id)
            client_name = client.client_name

        if fs_options is None:
            fs_options = {}

        request_json = {
            "taskInfo": {
                "associations": [self._restore_association],
                "task": self._task,
                "subTasks": [{
                    "subTaskOperation": 1,
                    "subTask": self._restore_sub_task,
                    "options": {
                        "restoreOptions": {
                            "browseOption": {
                                "mediaOption": {}
                            },
                            "commonOptions": {
                                "unconditionalOverwrite": overwrite,
                                "preserveLevel": fs_options.get("preserve_level", 1),
                                "stripLevel": 2,
                                "stripLevelType": 0
                            },
                            "impersonation": {},
                            "destination": {
                                "inPlace": in_place,
                                "destClient": {
                                    "clientId": client_id,
                                    "clientName": client_name,
                                }
                            },
                            "fileOption": {
                                "sourceItem": paths
                            }
                        }
                    }
                }]
            }
        }

        if restore_data_and_acl:
            request_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]["restoreACLsType"] = 3

        if destination_path is not None:
            request_json['taskInfo']["subTasks"][0]["options"][
                "restoreOptions"]["destination"]["destPath"] = [destination_path]

        if copy_precedence:
            temp = {
                "copyPrecedence": {
                    "copyPrecedenceApplicable": True,
                    "synchronousCopyPrecedence": copy_precedence,
                    "copyPrecedence": copy_precedence
                }
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'browseOption']['mediaOption'].update(temp)

        if fs_options.get("proxy_client"):
            temp = {
                "proxyForSnapClients":
                {
                    "clientName": fs_options.get("proxy_client", '')
                }
            }

            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'browseOption']['mediaOption'].update(temp)

        if fs_options.get("impersonate_user"):
            temp = {
                "useImpersonation": True,
                "user": {
                    "userName": fs_options['impersonate_user'],
                    "password": fs_options['impersonate_password']
                }
            }

            request_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['impersonation'] = temp

        restore_option = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']

        if from_time and (from_time != '01/01/1970 00:00:00' and from_time != '1/1/1970 00:00:00'):
            temp = {
                "browseOption": {
                    "timeRange": {
                        "fromTimeValue": from_time
                    }
                }
            }

            if 'browseOption' in restore_option:
                if 'timeRange' in restore_option['browseOption']:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption']['timeRange'].update(temp['browseOption']['timeRange'])
                else:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption'].update(temp['browseOption'])
            else:
                request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(temp)

        if to_time and (to_time != '01/01/1970 00:00:00' and to_time != '1/1/1970 00:00:00'):
            temp = {
                "browseOption": {
                    "timeRange": {
                        "toTimeValue": to_time
                    }
                }
            }

            if 'browseOption' in restore_option:
                if 'timeRange' in restore_option['browseOption']:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption']['timeRange'].update(temp['browseOption']['timeRange'])
                else:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption'].update(temp['browseOption'])
            else:
                request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(temp)

        return request_json

    def _restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None):
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

            Returns:
                object - instance of the Job class for this restore job

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
            to_time=to_time)

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
            fs_options=None):
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

            Returns:
                object - instance of the Job class for this restore job

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
            fs_options=fs_options
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
        """Browses the content of a Backupset.

            Args:
                Dictionary of browse options:
                    Example:
                        browse({
                            'path': 'c:\\hello',
                            'show_deleted': True,
                            'from_time': '2014-04-20 12:00:00',
                            'to_time': '2016-04-21 12:00:00'
                        })

                    (OR)

                Keyword argument of browse options:
                    Example:
                        browse(
                            path='c:\\hello',
                            show_deleted=True,
                            from_time='2014-04-20 12:00:00',
                            to_time='2016-04-21 12:00:00'
                        )

                Refer self._default_browse_options for all the supported options

        Returns:
            list - List of only the file, folder paths from the browse response

            dict - Dictionary of all the paths with additional metadata retrieved from browse

        Raises:
            SDKException:
                if there are more than one backupsets in the instance
        """
        all_backupsets = self.backupsets._backupsets

        # do browse operation if there is only one backupset in the instance
        # raise `SDKException` if there is more than one backupset in the instance

        if len(all_backupsets) == 1:
            backupset_name = all_backupsets.keys()[0]
            temp_backupset_obj = self.backupsets.get(backupset_name)
            return temp_backupset_obj.browse(*args, **kwargs)
        else:
            raise SDKException('Instance', '104')

    def find(self, *args, **kwargs):
        """Searches a file/folder in the backupset backup content,
            and returns all the files matching the filters given.

         Args:
            Dictionary of find options:
                Example:
                    find({
                        'file_name': '*.txt',
                        'show_deleted': True,
                        'from_time': '2014-04-20 12:00:00',
                        'to_time': '2016-04-21 12:00:00'
                    })

                (OR)

            Keyword argument of find options:
                Example:
                    find(
                        file_name='*.txt',
                        show_deleted=True,
                        from_time=2014-04-20 12:00:00,
                        to_time='2016-04-21 12:00:00'
                    )

            Refer self._default_browse_options for all the supported options

            Additional options supported:
                file_name       (str)   --   Find files with name

                file_size_gt    (int)   --   Find files with size greater than size

                file_size_lt    (int)   --   Find files with size lesser than size

                file_size_et    (int)   --   Find files with size equal to size

        Returns:
            list - List of only the file, folder paths from the browse response

            dict - Dictionary of all the paths with additional metadata retrieved from browse

        Raises:
            SDKException:
                if there are more than one backupsets in the instance
        """
        all_backupsets = self.backupsets._get_backupsets()

        # do find operation if there is only one backupset in the instance
        # raise `SDKException` if there is more than one backupset in the instance

        if len(all_backupsets) == 1:
            backupset_name = all_backupsets.keys()[0]
            temp_backupset_obj = self.backupsets.get(backupset_name)
            return temp_backupset_obj.find(*args, **kwargs)
        else:
            raise SDKException('Instance', '104')
