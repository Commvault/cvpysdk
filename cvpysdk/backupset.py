#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing backup set operations.

Backupsets and Backupset are 2 classes defined in this file.

Backupsets: Class for representing all the backup sets associated with a specific agent

Backupset:  Class for a single backup set selected for an agent,
                and to perform operations on that backup set


Backupsets:
    __init__(class_object)          -- initialise object of Backupsets class associated with
                                           the specified agent/instance

    __str__()                       -- returns all the backupsets associated with the agent

    __repr__()                      -- returns the string for the instance of the Backupsets class

    _get_backupsets()               -- gets all the backupsets associated with the agent specified

    has_backupset(backupset_name)   -- checks if a backupset exists with the given name or not

    add(backupset_name)             -- adds a new backupset to the agent of the specified client

    get(backupset_name)             -- returns the Backupset class object
                                           of the input backup set name

    delete(backupset_name)          -- removes the backupset from the agent of the specified client


Backupset:
    __init__(agent_object,
             backupset_name,
             backupset_id=None,
             instance_id=1,
             instance_name=None)    -- initialise object of Backupset with the specified backupset
                                         name and id, and associated to the specified agent

    __repr__()                      -- return the backupset name, the instance is associated with

    _get_backupset_id()             -- method to get the backupset id, if not specified in __init__

    _get_backupset_properties()     -- get the properties of this backupset

    _run_backup(subclient_name,
                return_list)        -- runs full backup for the specified subclient,
                                        and appends the job object to the return list

    _update()                       -- updates the properties of the backupset

    set_default_backupset()         -- sets the backupset as the default backup set for the agent,
                                        if not already default

    backup()                        -- runs full backup for all subclients
                                        associated with this backupset

"""

from __future__ import absolute_import

import threading

from .subclient import Subclients
from .schedules import Schedules
from .exception import SDKException


class Backupsets(object):
    """Class for getting all the backupsets associated with a client."""

    def __init__(self, class_object):
        """Initialize object of the Backupsets class.

            Args:
                class_object (object)  --  instance of the Agent/Instance class

            Returns:
                object - instance of the Backupsets class
        """
        from .agent import Agent
        from .instance import Instance

        self._instance_object = None

        if isinstance(class_object, Agent):
            self._agent_object = class_object
        elif isinstance(class_object, Instance):
            self._instance_object = class_object
            self._agent_object = class_object._agent_object

        self._commcell_object = self._agent_object._commcell_object

        self._BACKUPSETS = (self._commcell_object._services.GET_ALL_BACKUPSETS) % (
            self._agent_object._client_object.client_id
        )

        if self._agent_object.agent_name in ['cloud apps', 'sql server']:
            self._BACKUPSETS += '&excludeHidden=0'

        self._backupsets = self._get_backupsets()

    def __str__(self):
        """Representation string consisting of all backupsets of the agent of a client.

            Returns:
                str - string of all the backupsets of an agent of a client
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Backupset', 'Instance', 'Agent', 'Client'
        )

        for index, backupset in enumerate(self._backupsets):
            sub_str = '{:^5}\t{:20}\t{:20}\t{:20}\t{:20}\n'.format(
                index + 1,
                backupset.split('\\')[-1],
                self._backupsets[backupset]['instance'],
                self._agent_object.agent_name,
                self._agent_object._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Backupsets class."""
        return "Backupsets class instance for Agent: '{0}'".format(self._agent_object.agent_name)

    def _get_backupsets(self):
        """Gets all the backupsets associated to the agent specified by agent_object.

            Returns:
                dict - consists of all backupsets of the agent
                    {
                         "backupset1_name": {
                             "id": backupset1_id,
                             "instance": instance
                         },
                         "backupset2_name": {
                             "id": backupset2_id,
                             "instance": instance
                         }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._BACKUPSETS
        )

        if flag:
            if response.json() and 'backupsetProperties' in response.json():
                return_dict = {}

                for dictionary in response.json()['backupsetProperties']:
                    agent = str(dictionary['backupSetEntity']['appName']).lower()
                    instance = str(dictionary['backupSetEntity']['instanceName']).lower()

                    if self._instance_object is not None:
                        if (self._instance_object.instance_name in instance and
                                self._agent_object.agent_name in agent):
                            temp_name = str(dictionary['backupSetEntity']['backupsetName']).lower()
                            temp_id = str(dictionary['backupSetEntity']['backupsetId']).lower()
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "instance": instance
                            }
                    elif self._agent_object.agent_name in agent:
                        temp_name = str(dictionary['backupSetEntity']['backupsetName']).lower()
                        temp_id = str(dictionary['backupSetEntity']['backupsetId']).lower()

                        if len(self._agent_object.instances._instances) > 1:
                            return_dict["{0}\\{1}".format(instance, temp_name)] = {
                                "id": temp_id,
                                "instance": instance
                            }
                        else:
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "instance": instance
                            }

                return return_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_backupset(self, backupset_name):
        """Checks if a backupset exists for the agent with the input backupset name.

            Args:
                backupset_name (str)  --  name of the backupset

            Returns:
                bool - boolean output whether the backupset exists for the agent or not

            Raises:
                SDKException:
                    if type of the backupset name argument is not string
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '101')

        return self._backupsets and str(backupset_name).lower() in self._backupsets

    def add(self, backupset_name, on_demand_backupset=False):
        """Adds a new backup set to the agent.

            Args:
                backupset_name      (str)   --  name of the new backupset to add

                on_demand_backupset (bool)  --  flag to specify whether the backupset to be added
                                                    is a simple backupset or an on-demand backupset
                    default: False

            Returns:
                object - instance of the Backupset class, if created successfully

            Raises:
                SDKException:
                    if type of the backupset name argument is not string

                    if failed to create a backupset

                    if response is empty

                    if response is not success

                    if backupset with same name already exists
        """
        if not (isinstance(backupset_name, str) and isinstance(on_demand_backupset, bool)):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = str(backupset_name).lower()

        if self.has_backupset(backupset_name):
            raise SDKException(
                'Backupset', '102', 'Backupset "{0}" already exists.'.format(backupset_name)
            )

        add_backupset_service = self._commcell_object._services.ADD_BACKUPSET

        if self._instance_object is None:
            if self._agent_object.instances.has_instance('DefaultInstanceName'):
                self._instance_object = self._agent_object.instances.get('DefaultInstanceName')
            else:
                self._instance_object = self._agent_object.instances.get(
                    sorted(self._agent_object.instances._instances)[0]
                )

        request_json = {
            "association": {
                "entity": [{
                    "clientName": self._agent_object._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": backupset_name
                }]
            },
            "backupSetInfo": {
                "commonBackupSet": {
                    "onDemandBackupset": on_demand_backupset
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_backupset_service, request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    response_value = response.json()['response'][0]
                    error_code = str(response_value['errorCode'])
                    error_message = None

                    if 'errorString' in response_value:
                        error_message = str(response_value['errorString'])

                    if error_message:
                        o_str = 'Failed to create new backupset\nError: "{0}"'.format(
                            error_message
                        )
                        raise SDKException('Backupset', '102', o_str)
                    else:
                        if error_code == '0':
                            backupset_id = response_value['entity']['backupsetId']

                            # initialize the backupsets again
                            # so the backupsets object has all the backupsets
                            self._backupsets = self._get_backupsets()

                            return Backupset(
                                self._instance_object,
                                backupset_name,
                                backupset_id
                            )
                        else:
                            o_str = ('Failed to create new backupset with error code: "{0}"\n'
                                     'Please check the documentation for '
                                     'more details on the error').format(error_code)

                            raise SDKException('Backupset', '102', o_str)
                else:
                    error_code = response.json()['errorCode']
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to create new backupset\nError: "{0}"'.format(
                        error_message
                    )
                    raise SDKException('Backupset', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, backupset_name):
        """Returns a backupset object of the specified backupset name.

            Args:
                backupset_name (str)  --  name of the backupset

            Returns:
                object - instance of the Backupset class for the given backupset name

            Raises:
                SDKException:
                    if type of the backupset name argument is not string

                    if no backupset exists with the given name
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = str(backupset_name).lower()

            if self.has_backupset(backupset_name):
                if self._instance_object is None:
                    self._instance_object = self._agent_object.instances.get(
                        self._backupsets[backupset_name]['instance']
                    )

                return Backupset(
                    self._instance_object,
                    backupset_name,
                    self._backupsets[backupset_name]["id"]
                )

            raise SDKException(
                'Backupset', '102', 'No backupset exists with name: "{0}"'.format(backupset_name)
            )

    def delete(self, backupset_name):
        """Deletes the backup set from the agent.

            Args:
                backupset_name (str)  --  name of the backupset

            Raises:
                SDKException:
                    if type of the backupset name argument is not string

                    if failed to delete the backupset

                    if response is empty

                    if response is not success

                    if no backupset exists with the given name
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = str(backupset_name).lower()

        if self.has_backupset(backupset_name):
            delete_backupset_service = self._commcell_object._services.BACKUPSET % (
                self._backupsets[backupset_name]['id']
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', delete_backupset_service
            )

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = str(response_value['errorString'])

                        if error_message:
                            o_str = 'Failed to delete backupset\nError: "{0}"'
                            raise SDKException('Backupset', '102', o_str.format(error_message))
                        else:
                            if error_code == '0':
                                # initialize the backupsets again
                                # so the backupsets object has all the backupsets
                                self._backupsets = self._get_backupsets()
                            else:
                                o_str = ('Failed to delete backupset with error code: "{0}"\n'
                                         'Please check the documentation for '
                                         'more details on the error').format(error_code)
                                raise SDKException('Backupset', '102', o_str)
                    else:
                        error_code = response.json()['errorCode']
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to delete backupset\nError: "{0}"'.format(error_message)
                        raise SDKException('Backupset', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Backupset', '102', 'No backupset exists with name: "{0}"'.format(backupset_name)
            )


class Backupset(object):
    """Class for performing backupset operations for a specific backupset."""

    def __init__(self, instance_object, backupset_name, backupset_id=None):
        """Initialise the backupset object.

            Args:
                instance_object     (object)  --  instance of the Instance class

                backupset_name      (str)     --  name of the backupset

                backupset_id        (str)     --  id of the backupset
                    default: None

            Returns:
                object - instance of the Backupset class
        """
        self._instance_object = instance_object
        self._agent_object = self._instance_object._agent_object
        self._commcell_object = self._instance_object._agent_object._commcell_object

        self._backupset_name = str(backupset_name).split('\\')[-1].lower()
        self._description = None

        if backupset_id:
            # Use the backupset id provided in the arguments
            self._backupset_id = str(backupset_id)
        else:
            # Get the id associated with this backupset
            self._backupset_id = self._get_backupset_id()

        self._BACKUPSET = self._commcell_object._services.BACKUPSET % (self.backupset_id)

        self._is_default = False
        self._properties = None

        self._get_backupset_properties()

        self.subclients = Subclients(self)
        self.schedules = Schedules(self)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = ('Backupset class instance for Backupset: "{0}" '
                                 'for Instance: "{1}" of Agent: "{2}"')
        return representation_string.format(
            self.backupset_name,
            self._instance_object.instance_name,
            self._instance_object._agent_object.agent_name
        )

    def _get_backupset_id(self):
        """Gets the backupset id associated with this backupset.

            Returns:
                str - id associated with this backupset
        """
        backupsets = Backupsets(self._instance_object)
        return backupsets.get(self.backupset_name).backupset_id

    def _get_backupset_properties(self):
        """Gets the properties of this backupset.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._BACKUPSET)

        if flag:
            if response.json() and "backupsetProperties" in response.json():
                self._properties = response.json()["backupsetProperties"][0]

                backupset_name = self._properties["backupSetEntity"]["backupsetName"]
                self._backupset_name = str(backupset_name).lower()

                self._is_default = bool(self._properties["commonBackupSet"]["isDefaultBackupSet"])

                if "userDescription" in self._properties["commonBackupSet"]:
                    self._description = str(self._properties["commonBackupSet"]["userDescription"])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _run_backup(self, subclient_name, return_list):
        """Triggers full backup job for the given subclient, and appends its Job object to the list.
            The SDKExcpetion class instance is appended to the list,
            if any exception is raised while running the backup job for the Subclient.

            Args:
                subclient_name (str)   --  name of the subclient to trigger the backup for

                return_list    (list)  --  list to append the job object to
        """
        try:
            job = self.subclients.get(subclient_name).backup()
            if job:
                return_list.append(job)
        except SDKException as excp:
            return_list.append(excp)

    def _update(self, backupset_name, backupset_description, default_backupset):
        """Updates the properties of the backupset.

            Args:
                backupset_name        (str)   --  new name of the backupset

                backupset_description (str)   --  description of the backupset

                default_backupset     (bool)  --  default backupset property

            Returns:
                (bool, str, str):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        request_json = {
            "association": {
                "entity": [{
                    "clientName": self._instance_object._agent_object._client_object.client_name,
                    "appName": self._instance_object._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": self.backupset_name
                }]
            },
            "backupsetProperties": {
                "commonBackupSet": {
                    "newBackupSetName": backupset_name,
                    "isDefaultBackupSet": default_backupset
                }
            }
        }

        if backupset_description is not None:
            request_json["backupsetProperties"]["commonBackupSet"][
                "userDescription"] = backupset_description

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._BACKUPSET, request_json
        )

        self._get_backupset_properties()

        if flag:
            if response.json() and "response" in response.json():
                error_code = str(response.json()["response"][0]["errorCode"])

                if error_code == "0":
                    return (True, "0", "")
                else:
                    error_string = ""

                    if "errorString" in response.json()["response"][0]:
                        error_string = response.json()["response"][0]["errorString"]

                    if error_string:
                        return (False, error_code, error_string)
                    else:
                        return (False, error_code, "")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def backupset_id(self):
        """Treats the backupset id as a read-only attribute."""
        return self._backupset_id

    @property
    def backupset_name(self):
        """Treats the backupset name as a property of the Backupset class."""
        return self._backupset_name

    @property
    def description(self):
        """Treats the backupset description as a property of the Backupset class."""
        return self._description

    @property
    def is_default_backupset(self):
        """Treats the is default backupset as a read-only attribute."""
        return self._is_default

    @backupset_name.setter
    def backupset_name(self, value):
        """Sets the name of the backupset as the value provided as input.

            Raises:
                SDKException:
                    if failed to update the backupset name

                    if type of value input is not string
        """
        if isinstance(value, str):
            output = self._update(
                backupset_name=value,
                backupset_description=self.description,
                default_backupset=self.is_default_backupset
            )

            if output[0]:
                return
            else:
                o_str = 'Failed to update the name of the backupset\nError: "{0}"'
                raise SDKException('Backupset', '102', o_str.format(output[2]))
        else:
            raise SDKException('Backupset', '102', 'Backupset name should be a string value')

    @description.setter
    def description(self, value):
        """Sets the description of the backupset as the value provided as input.

            Raises:
                SDKException:
                    if failed to update the backupset description

                    if type of value input is not string

                    if description cannot be modified for this backupset
        """
        if self.description is not None:
            if isinstance(value, str):
                output = self._update(
                    backupset_name=self.backupset_name,
                    backupset_description=value,
                    default_backupset=self.is_default_backupset
                )

                if output[0]:
                    return
                else:
                    o_str = 'Failed to update the description of the backupset\nError: "{0}"'
                    raise SDKException('Backupset', '102', o_str.format(output[2]))
            else:
                raise SDKException(
                    'Backupset', '102', 'Backupset description should be a string value'
                )
        else:
            raise SDKException('Backupset', '102', 'Description cannot be modified')

    def set_default_backupset(self):
        """Sets the backupset represented by this Backupset class instance as the default backupset
            if it is not the default backupset.

            Raises:
                SDKException:
                    if failed to set this as the default backupset
        """
        if self.is_default_backupset is False:
            output = self._update(
                backupset_name=self.backupset_name,
                backupset_description=self.description,
                default_backupset=True
            )

            if output[0]:
                return
            else:
                o_str = 'Failed to set this as the Default Backup Set\nError: "{0}"'
                raise SDKException('Backupset', '102', o_str.format(output[2]))

    def backup(self):
        """Run full backup job for all subclients in this backupset.

            Returns:
                list - list containing the job objects for the full backup jobs started for
                        the subclients in the backupset
        """
        return_list = []
        thread_list = []

        all_subclients = self.subclients._subclients

        if all_subclients:
            for subclient in all_subclients:
                thread = threading.Thread(
                    target=self._run_backup, args=(subclient, return_list)
                )
                thread_list.append(thread)
                thread.start()

        for thread in thread_list:
            thread.join()

        return return_list
