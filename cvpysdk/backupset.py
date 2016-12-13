#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing backup set operations.

Backupsets and Backupset are 2 classes defined in this file.

Backupsets: Class for representing all the backup sets associated with a specific agent

Backupset:  Class for a single backup set selected for an agent,
                and to perform operations on that backup set


Backupsets:
    __init__(agent_object)          -- initialise object of Backupsets class associated with
                                        the specified agent
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
             instance_name=None)    -- initialise object of Backupset with the specified agent name
                                         and id, and associated to the specified agent
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

import string
import threading

from subclient import Subclients
from schedules import Schedules
from exception import SDKException


class Backupsets(object):
    """Class for getting all the backupsets associated with a client."""

    def __init__(self, agent_object):
        """Initialize object of the Backupsets class.

            Args:
                agent_object (object)  --  instance of the Agent class

            Returns:
                object - instance of the Backupsets class
        """
        self._agent_object = agent_object
        self._commcell_object = self._agent_object._commcell_object
        self._ALL_BACKUPSETS = self._commcell_object._services.GET_ALL_BACKUPSETS % (
            self._agent_object._client_object.client_id
        )

        self._instance_name = None
        self._instance_id = None
        self._backupsets = self._get_backupsets()

    def __str__(self):
        """Representation string consisting of all backupsets of the agent of a client.

            Returns:
                str - string of all the backupsets of an agent of a client
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Backupset', 'Agent', 'Client')

        for index, backupset in enumerate(self._backupsets):
            sub_str = '{:^5}\t{:20}\t{:20}\t{:20}\n'.format(
                index + 1,
                backupset,
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
                         "backupset1_name": backupset1_id,
                         "backupset2_name": backupset2_id
                    }

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET',
                                                                            self._ALL_BACKUPSETS)

        if flag:
            if response.json() and 'backupsetProperties' in response.json().keys():
                return_dict = {}

                for dictionary in response.json()['backupsetProperties']:
                    if not self._instance_name:
                        self._instance_name = str(dictionary['backupSetEntity']['instanceName'])
                        self._instance_id = str(dictionary['backupSetEntity']['instanceId'])

                    agent = str(dictionary['backupSetEntity']['appName']).lower()

                    if self._agent_object.agent_name in agent:
                        temp_name = str(dictionary['backupSetEntity']['backupsetName']).lower()
                        temp_id = str(dictionary['backupSetEntity']['backupsetId']).lower()
                        return_dict[temp_name] = temp_id

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
            raise SDKException('Backupset', '103')

        return self._backupsets and str(backupset_name).lower() in self._backupsets

    def add(self, backupset_name, on_demand_backupset=False):
        """Adds a new backup set to the agent.

            Args:
                backupset_name (str)        --  name of the new backupset to add
                on_demand_backupset (bool)  --  flag to specify whether the backupset to be added
                                                    is normal backupset or an on-demand backupset

            Returns:
                object - instance of the Backupset class, if created successfully
                None - if failed to add new backup set

            Raises:
                SDKException:
                    if type of the backupset name argument is not string
                    if response is empty
                    if response is not success
                    if backupset with same name already exists
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '103')
        else:
            backupset_name = str(backupset_name).lower()

        if not self.has_backupset(backupset_name):
            add_backupset_service = self._commcell_object._services.ADD_BACKUPSET

            request_json = {
                "App_CreateBackupSetRequest": {
                    "association": {
                        "entity": {
                            "appName": self._agent_object.agent_name,
                            "backupsetName": backupset_name,
                            "clientName": self._agent_object._client_object.client_name,
                            "instanceName": self._instance_name
                        }
                    },
                    "backupSetInfo": {
                        "commonBackupSet": {
                            "onDemandBackupset": 1 if on_demand_backupset else 0
                        }
                    }
                }
            }

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', add_backupset_service, request_json)

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = str(response_value['errorString'])

                        if error_message:
                            o_str = 'Failed to create new backupset with error code: "{0}", error: "{1}"'
                            print o_str.format(error_code, error_message)
                        else:
                            if error_code is '0':
                                print 'Backupset "{0}" created successfully'.format(backupset_name)

                                backupset_id = response_value['entity']['backupsetId']

                                # initialize the backupsets again
                                # so the backupsets object has all the backupsets
                                self._backupsets = self._get_backupsets()

                                return Backupset(self._agent_object,
                                                 backupset_name,
                                                 backupset_id,
                                                 self._instance_id)
                            else:
                                o_str = 'Failed to create new backupset with error code: "{0}"'
                                print o_str.format(error_code)
                                print 'Please check the documentation for more details on the error'
                    else:
                        error_code = response.json()['errorCode']
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to create new backupset with error code: "{0}", error: "{1}"'
                        print o_str.format(error_code, error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException('Backupset',
                               '102',
                               'Backupset "{0}" already exists.'.format(backupset_name))

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
            raise SDKException('Backupset', '103')
        else:
            backupset_name = str(backupset_name).lower()

            if self.has_backupset(backupset_name):
                return Backupset(self._agent_object,
                                 backupset_name,
                                 self._backupsets[backupset_name],
                                 self._instance_id,
                                 self._instance_name)

            raise SDKException('Backupset',
                               '102',
                               'No backupset exists with name: "{0}"'.format(backupset_name))

    def delete(self, backupset_name):
        """Deletes the backup set from the agent.

            Args:
                backupset_name (str)  --  name of the backupset

            Returns:
                None

            Raises:
                SDKException:
                    if type of the backupset name argument is not string
                    if response is empty
                    if response is not success
                    if no backupset exists with the given name
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '103')
        else:
            backupset_name = str(backupset_name).lower()

        if self.has_backupset(backupset_name):
            delete_backupset_service = self._commcell_object._services.BACKUPSET % \
                (self._backupsets[backupset_name])

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', delete_backupset_service)

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = str(response_value['errorString'])

                        if error_message:
                            o_str = 'Failed to delete backupset with error code: "{0}", error: "{1}"'
                            print o_str.format(error_code, error_message)
                        else:
                            if error_code is '0':
                                print 'Backupset "{0}" deleted successfully'.format(backupset_name)

                                # initialize the backupsets again
                                # so the backupsets object has all the backupsets
                                self._backupsets = self._get_backupsets()
                            else:
                                o_str = 'Failed to delete backupset with error code: "{0}"'
                                print o_str.format(error_code)
                                print 'Please check the documentation for more details on the error'
                    else:
                        error_code = response.json()['errorCode']
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to delete backupset with error code: "{0}", error: "{1}"'
                        print o_str.format(error_code, error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException('Backupset',
                               '102',
                               'No backupset exists with name: "{0}"'.format(backupset_name))


class Backupset(object):
    """Class for performing backupset operations for a specific backupset."""

    def __init__(
            self,
            agent_object,
            backupset_name,
            backupset_id=None,
            instance_id=1,
            instance_name=None):
        """Initialise the backupset object.

            Args:
                agent_object (object)  --  instance of the Agent class
                backupset_name (str)   --  name of the backupset
                backupset_id (str)     --  id of the backupset
                    default: None
                instance_id (str)      --  id of the instance associated with the backupset
                    default: 1, for File System iDA

            Returns:
                object - instance of the Backupset class
        """
        self._agent_object = agent_object
        self._commcell_object = self._agent_object._commcell_object

        self._backupset_name = str(backupset_name).lower()
        self._description = ""
        self._instance_id = instance_id

        if instance_name:
            self._instance_name = instance_name

        if backupset_id:
            # Use the backupset id provided in the arguments
            self._backupset_id = str(backupset_id)
        else:
            # Get the id associated with this backupset
            self._backupset_id = self._get_backupset_id()

        self._BACKUPSET = self._commcell_object._services.BACKUPSET % (self.backupset_id)

        self._is_default = False

        self._properties = self._get_backupset_properties()

        self.subclients = Subclients(self)
        self.schedules = Schedules(self)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Backupset class instance for Backupset: "{0}" of Agent: "{1}"'
        return representation_string.format(self.backupset_name, self._agent_object.agent_name)

    def _get_backupset_id(self):
        """Gets the backupset id associated with this backupset.

            Returns:
                str - id associated with this backupset
        """
        backupsets = Backupsets(self._agent_object)
        return backupsets.get(self.backupset_name).backupset_id

    def _get_backupset_properties(self):
        """Gets the properties of this backupset.

            Returns:
                str - properties of the backupset
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET',
                                                                            self._BACKUPSET)

        if flag:
            if response.json() and "backupsetProperties" in response.json():
                properties = response.json()["backupsetProperties"][0]

                self._backupset_name = str(properties["backupSetEntity"]["backupsetName"]).lower()
                self._description = str(properties["commonBackupSet"]["userDescription"])
                self._is_default = bool(properties["commonBackupSet"]["isDefaultBackupSet"])

                o_str = '\nProperties of Backupset: "{0}"'.format(self.backupset_name)
                o_str += '\n\tClient: \t{0}'.format(properties["backupSetEntity"]["clientName"])
                o_str += '\n\tAgent: \t\t{0}\n'.format(properties["backupSetEntity"]["appName"])
                o_str += '\tInstance: \t{0}'.format(properties["backupSetEntity"]["instanceName"])

                if self.description:
                    o_str += '\n\n\tDescription: \t{0}'.format(self.description)
                else:
                    o_str += '\n\n\tDescription: \t  ----  '

                return o_str.strip()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _run_backup(self, subclient_name, return_list):
        """Triggers full backup job for the given subclient, and appeds its job object to the list.

            Args:
                subclient_name (str)  --  name of the subclient to trigger the backup for
                return_list (list)    --  list to append the job object to

            Returns:
                None

            Prints the exception message in case any exception is raised.
        """
        try:
            job = self.subclients.get(subclient_name).backup()
            if job:
                return_list.append(job)
        except SDKException as excp:
            print excp.exception_message

    def _update(self, backupset_name, backupset_description, default_backupset):
        """Updates the properties of the backupset.

            Args:
                backupset_name        (str)     --  new name of the backupset
                backupset_description (str)     --  description of the backupset
                default_backupset     (bool)    --  default backupset property

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
            "App_SetBackupsetPropertiesRequest": {
                "association": {
                    "entity": {
                        "appName": self._agent_object.agent_name,
                        "clientName": self._agent_object._client_object.client_name,
                        "instanceName": self._instance_name,
                        "backupsetName": self.backupset_name
                    }
                },
                "backupsetProperties": {
                    "commonBackupSet": {
                        "newBackupSetName": backupset_name,
                        "userDescription": backupset_description,
                        "isDefaultBackupSet": default_backupset
                    }
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            self._BACKUPSET,
                                                                            request_json)

        if flag:
            if response.json() and "response" in response.json():
                error_code = str(response.json()["response"][0]["errorCode"])

                self._properties = self._get_backupset_properties()

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
    def properties(self):
        """Treats the backupset properties as a read-only attribute."""
        return self._properties

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
        """Treats the backupset default flag as a property of the Backupset class."""
        return self._is_default

    @backupset_name.setter
    def backupset_name(self, value):
        """Sets the name of the backupset as the value provided as input."""
        if isinstance(value, str):
            output = self._update(
                backupset_name=value,
                backupset_description=self.description,
                default_backupset=self.is_default_backupset)

            if output[0]:
                print "Backupset Name updated successfully"
            else:
                print "Failed to update the name of the backupset."
                print "Error Code: {0}, Error Message: {1}".format(output[1], output[2])
                print "Please check the documentation for more details on the error"
        else:
            raise SDKException('Backupset', '102', 'Backupset name should be a string value')

    @description.setter
    def description(self, value):
        """Sets the description of the backupset as the value provided as input."""
        if isinstance(value, str):
            output = self._update(
                backupset_name=self.backupset_name,
                backupset_description=value,
                default_backupset=self.is_default_backupset)

            if output[0]:
                print "Backupset Description updated successfully"
            else:
                print "Failed to update the description of the backupset."
                print "Error Code: {0}, Error Message: {1}".format(output[1], output[2])
                print "Please check the documentation for more details on the error"
        else:
            raise SDKException(
                'Backupset',
                '102',
                'Backupset description should be a string value')

    def set_default_backupset(self):
        """Sets the backupset represented by this Backupset class instance as the default backupset
            if it is not the default backupset."""
        if self.is_default_backupset is False:
            output = self._update(
                backupset_name=self.backupset_name,
                backupset_description=self.description,
                default_backupset=True)

            if output[0]:
                o_str = 'Backupset: "{0}" set to DefaultBackupSet for "{1}" agent of Client: "{2}"'
                print o_str.format(
                    self.backupset_name,
                    string.capwords(self._agent_object.agent_name),
                    self._agent_object._client_object.client_name
                )
            else:
                print "Failed to set this backupset as the default backup set."
                print "Error Code: {0}, Error Message: {1}".format(output[1], output[2])
                print "Please check the documentation for more details on the error"

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
