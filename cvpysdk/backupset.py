# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing backup set operations.

Backupsets and Backupset are 2 classes defined in this file.

Backupsets: Class for representing all the backup sets associated with a specific agent

Backupset:  Class for a single backup set selected for an agent,
and to perform operations on that backup set


Backupsets:
===========
    __init__(class_object)          -- initialise object of Backupsets class associated with
    the specified agent/instance

    __str__()                       -- returns all the backupsets associated with the agent

    __repr__()                      -- returns the string for the instance of the Backupsets class

    __len__()                       -- returns the number of backupsets associated with the Agent

    __getitem__()                   -- returns the name of the backupset for the given backupset Id
    or the details for the given backupset name

    _get_backupsets()               -- gets all the backupsets associated with the agent specified

    default_backup_set()            -- returns the name of the default backup set

    all_backupsets()                -- returns the dict of all the backupsets for the Agent /
    Instance of the selected Client

    has_backupset(backupset_name)   -- checks if a backupset exists with the given name or not

    add(backupset_name)             -- adds a new backupset to the agent of the specified client

    get(backupset_name)             -- returns the Backupset class object
    of the input backup set name

    delete(backupset_name)          -- removes the backupset from the agent of the specified client

    refresh()                       -- refresh the backupsets associated with the agent


Backupset:
==========
    __init__()                      -- initialise object of Backupset with the specified backupset
    name and id, and associated to the specified instance

    __getattr__()                   -- provides access to restore helper methods

    __repr__()                      -- return the backupset name, the instance is associated with

    _get_backupset_id()             -- method to get the backupset id, if not specified in __init__

    _get_backupset_properties()     -- get the properties of this backupset

    _run_backup()                   -- runs full backup for the specified subclient,
    and appends the job object to the return list

    _update()                       -- updates the properties of the backupset

    _get_epoch_time()               -- gets the Epoch time given the input time is in format

                                            %Y-%m-%d %H:%M:%S

    _set_defaults()                 -- recursively sets default values on a dictionary

    _prepare_browse_options()       -- prepares the options for the Browse/find operation

    _prepare_browse_json()          -- prepares the JSON object for the browse request

    _process_browse_response()      -- retrieves the items from browse response

    _do_browse()                    -- performs a browse operation with the given options

    set_default_backupset()         -- sets the backupset as the default backup set for the agent,
    if not already default

    backup()                        -- runs full backup for all subclients
    associated with this backupset

    browse()                        -- browse the content of the backupset

    find()                          -- find content in the backupset

    refresh()                       -- refresh the properties of the backupset

    delete_data()                   -- deletes items from the backupset and makes then unavailable
    to browse and restore

Backupset instance Attributes
-----------------------------
    **guid**                        -- treats the backupset GUID as a property
    of the Backupset class

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import threading
import time

from past.builtins import basestring

from .subclient import Subclients
from .schedules import Schedules
from .exception import SDKException


class Backupsets(object):
    """Class for getting all the backupsets associated with a client."""

    def __init__(self, class_object):
        """Initialize object of the Backupsets class.

            Args:
                class_object    (object)    --  instance of the Agent / Instance class

            Returns:
                object  -   instance of the Backupsets class

            Raises:
                SDKException:
                    if class object is not an instance of the Agent / Instance class

        """
        from .agent import Agent
        from .instance import Instance

        self._instance_object = None

        if isinstance(class_object, Agent):
            self._agent_object = class_object
        elif isinstance(class_object, Instance):
            self._instance_object = class_object
            self._agent_object = class_object._agent_object
        else:
            raise SDKException('Backupset', '103')

        self._client_object = self._agent_object._client_object

        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._BACKUPSETS = self._services['GET_ALL_BACKUPSETS'] % (self._client_object.client_id)

        from .backupsets.fsbackupset import FSBackupset
        from .backupsets.nasbackupset import NASBackupset
        from .backupsets.hanabackupset import HANABackupset
        from .backupsets.cabackupset import CloudAppsBackupset
        from .backupsets.postgresbackupset import PostgresBackupset
        from .backupsets.adbackupset import ADBackupset
        from .backupsets.db2backupset import DB2Backupset
        from .backupsets.vsbackupset import VSBackupset

        self._backupsets_dict = {
            'file system': FSBackupset,
            'nas': NASBackupset,        # SP11 or lower CS honors NAS as the Agent Name
            'ndmp': NASBackupset,       # SP12 and above honors NDMP as the Agent Name
            'sap hana': HANABackupset,
            'cloud apps': CloudAppsBackupset,
            'postgresql': PostgresBackupset,
            "active directory" : ADBackupset,
            'db2': DB2Backupset,
            'virtual server' : VSBackupset
        }

        if self._agent_object.agent_name in ['cloud apps', 'sql server', 'sap hana']:
            self._BACKUPSETS += '&excludeHidden=0'

        self._backupsets = None
        self._default_backup_set = None
        self.refresh()

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
                self._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Backupsets class."""
        return "Backupsets class instance for Agent: '{0}'".format(self._agent_object.agent_name)

    def __len__(self):
        """Returns the number of the backupsets for the selected Agent."""
        return len(self.all_backupsets)

    def __getitem__(self, value):
        """Returns the name of the backupset for the given backupset ID or
            the details of the backupset for given backupset Name.

            Args:
                value   (str / int)     --  Name or ID of the backupset

            Returns:
                str     -   name of the backupset, if the backupset id was given

                dict    -   dict of details of the backupset, if backupset name was given

            Raises:
                IndexError:
                    no backupset exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_backupsets:
            return self.all_backupsets[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_backupsets.items())
                )[0][0]
            except IndexError:
                raise IndexError('No backupset exists with the given Name / Id')

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
        flag, response = self._cvpysdk_object.make_request('GET', self._BACKUPSETS)

        if flag:
            if response.json() and 'backupsetProperties' in response.json():
                return_dict = {}

                for dictionary in response.json()['backupsetProperties']:
                    agent = dictionary['backupSetEntity']['appName'].lower()
                    instance = dictionary['backupSetEntity']['instanceName'].lower()

                    if self._instance_object is not None:
                        if (self._instance_object.instance_name in instance and
                                self._agent_object.agent_name in agent):
                            temp_name = dictionary['backupSetEntity']['backupsetName'].lower()
                            temp_id = str(dictionary['backupSetEntity']['backupsetId']).lower()
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "instance": instance
                            }

                            if dictionary['commonBackupSet'].get('isDefaultBackupSet'):
                                self._default_backup_set = temp_name

                    elif self._agent_object.agent_name in agent:
                        temp_name = dictionary['backupSetEntity']['backupsetName'].lower()
                        temp_id = str(dictionary['backupSetEntity']['backupsetId']).lower()

                        if len(self._agent_object.instances.all_instances) > 1:
                            return_dict["{0}\\{1}".format(instance, temp_name)] = {
                                "id": temp_id,
                                "instance": instance
                            }

                            if dictionary['commonBackupSet'].get('isDefaultBackupSet'):
                                self._default_backup_set = "{0}\\{1}".format(instance, temp_name)
                        else:
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "instance": instance
                            }

                            if dictionary['commonBackupSet'].get('isDefaultBackupSet'):
                                self._default_backup_set = temp_name

                return return_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_backupsets(self):
        """Returns the dict of backupsets for the Agent / Instance of the selected Client

            dict - consists of all backupsets
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
        """
        return self._backupsets

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
        if not isinstance(backupset_name, basestring):
            raise SDKException('Backupset', '101')

        return self._backupsets and backupset_name.lower() in self._backupsets

    def add(self, backupset_name, on_demand_backupset=False, **kwargs):
        """Adds a new backup set to the agent.

            Args:
                backupset_name      (str)   --  name of the new backupset to add

                on_demand_backupset (bool)  --  flag to specify whether the backupset to be added
                is a simple backupset or an on-demand backupset

                    default: False

                **kwargs    --  dict of keyword arguments as follows:

                    storage_policy  (str)   --  name of the storage policy to associate to the
                    backupset

                    plan_name       (str)   -- name of the plan to associate to the backupset


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
        if not (isinstance(backupset_name, basestring) and isinstance(on_demand_backupset, bool)):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = backupset_name.lower()

        if self.has_backupset(backupset_name):
            raise SDKException(
                'Backupset', '102', 'Backupset "{0}" already exists.'.format(backupset_name)
            )

        if self._instance_object is None:
            if self._agent_object.instances.has_instance('DefaultInstanceName'):
                self._instance_object = self._agent_object.instances.get('DefaultInstanceName')
            else:
                self._instance_object = self._agent_object.instances.get(
                    sorted(self._agent_object.instances.all_instances)[0]
                )

        request_json = {
            "association": {
                "entity": [{
                    "clientName": self._client_object.client_name,
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

        agent_settings = {
            'db2': """
request_json['backupSetInfo'].update({
    'db2BackupSet': {
        'dB2DefaultIndexSP': {
            'storagePolicyName': kwargs.get('storage_policy', '')
        }
    }
})
            """
        }

        exec(agent_settings.get(self._agent_object.agent_name, ''))

        if kwargs.get('plan_name'):
            plan_entity_dict = {
                "planName": kwargs.get('plan_name')
            }
            request_json['backupSetInfo']['planEntity'] = plan_entity_dict

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ADD_BACKUPSET'], request_json
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
                        o_str = 'Failed to create new backupset\nError: "{0}"'.format(
                            error_message
                        )
                        raise SDKException('Backupset', '102', o_str)
                    else:
                        if error_code == '0':
                            # initialize the backupsets again
                            # so the backupsets object has all the backupsets
                            self.refresh()

                            return self.get(backupset_name)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

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
        if not isinstance(backupset_name, basestring):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = backupset_name.lower()

            if self.has_backupset(backupset_name):
                if self._instance_object is None:
                    self._instance_object = self._agent_object.instances.get(
                        self._backupsets[backupset_name]['instance']
                    )

                if self._agent_object.agent_name in self._backupsets_dict.keys():
                    return self._backupsets_dict[self._agent_object.agent_name](
                        self._instance_object,
                        backupset_name,
                        self._backupsets[backupset_name]["id"]
                    )
                else:
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
        if not isinstance(backupset_name, basestring):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = backupset_name.lower()

        if self.has_backupset(backupset_name):
            delete_backupset_service = self._services['BACKUPSET'] % (
                self._backupsets[backupset_name]['id']
            )

            flag, response = self._cvpysdk_object.make_request('DELETE', delete_backupset_service)

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = response_value['errorString']

                        if error_message:
                            o_str = 'Failed to delete backupset\nError: "{0}"'
                            raise SDKException('Backupset', '102', o_str.format(error_message))
                        else:
                            if error_code == '0':
                                # initialize the backupsets again
                                # so the backupsets object has all the backupsets
                                self.refresh()
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
                raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException(
                'Backupset', '102', 'No backupset exists with name: "{0}"'.format(backupset_name)
            )

    def refresh(self):
        """Refresh the backupsets associated with the Agent / Instance."""
        self._backupsets = self._get_backupsets()

    @property
    def default_backup_set(self):
        """Returns the name of the default backup set for the selected Client and Agent."""
        return self._default_backup_set


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
        self._client_object = self._agent_object._client_object

        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._restore_methods = ['_process_restore_response', '_filter_paths', '_restore_json']

        self._backupset_name = backupset_name.split('\\')[-1].lower()
        self._description = None

        if backupset_id:
            # Use the backupset id provided in the arguments
            self._backupset_id = str(backupset_id)
        else:
            # Get the id associated with this backupset
            self._backupset_id = self._get_backupset_id()

        self._BACKUPSET = self._services['BACKUPSET'] % (self.backupset_id)
        self._BROWSE = self._services['BROWSE']
        self._RESTORE = self._services['RESTORE']

        self._is_default = False
        self._is_on_demand_backupset = False
        self._properties = None
        self._backupset_association = {}
        self._plan = None

        self.subclients = None
        self.schedules = None
        self.refresh()

        self._default_browse_options = {
            'operation': 'browse',
            'show_deleted': False,
            'from_time': 0,         # value should either be the Epoch time or the Timestamp
            'to_time': 0,           # value should either be the Epoch time or the Timestamp
            'path': '\\',
            'copy_precedence': 0,
            'media_agent': '',
            'page_size': 100000,
            'skip_node': 0,
            'restore_index': True,
            'vm_disk_browse': False,
            'filters': [],
            'job_id': 0,
            'commcell_id': self._commcell_object.commcell_id,
            'include_aged_data': False,
            'include_hidden': False,
            'include_running_jobs': False,
            'vs_volume_browse': False,
            'browse_view_name': 'VOLUMEVIEW',

            '_subclient_id': 0,
            '_raw_response': False
        }

    def __getattr__(self, attribute):
        """Returns the persistent attributes"""
        if attribute in self._restore_methods:
            return getattr(self._instance_object, attribute)

        return super(Backupset, self).__getattribute__(attribute)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = ('Backupset class instance for Backupset: "{0}" '
                                 'for Instance: "{1}" of Agent: "{2}"')
        return representation_string.format(
            self.backupset_name,
            self._instance_object.instance_name,
            self._agent_object.agent_name
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
        flag, response = self._cvpysdk_object.make_request('GET', self._BACKUPSET)

        if flag:
            if response.json() and "backupsetProperties" in response.json():
                self._properties = response.json()["backupsetProperties"][0]

                backupset_name = self._properties["backupSetEntity"]["backupsetName"]
                self._backupset_name = backupset_name.lower()

                self._backupset_association = self._properties['backupSetEntity']

                self._is_default = bool(self._properties["commonBackupSet"]["isDefaultBackupSet"])

                if 'commonBackupSet' in self._properties:
                    if 'onDemandBackupset' in self._properties['commonBackupSet']:
                        self._is_on_demand_backupset = bool(
                            self._properties['commonBackupSet']['onDemandBackupset']
                        )

                if "userDescription" in self._properties["commonBackupSet"]:
                    self._description = self._properties["commonBackupSet"]["userDescription"]

                if "planName" in self._properties["planEntity"]:
                    self._plan = self._commcell_object.plans.get(
                        self._properties["planEntity"]["planName"]
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _run_backup(self, subclient_name, return_list):
        """Triggers incremental backup job for the given subclient,
            and appends its Job object to the list.

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

    def _process_update_reponse(self, request_json):
        """Runs the Backupset update API with the request JSON provided,
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
        flag, response = self._cvpysdk_object.make_request('POST', self._BACKUPSET, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _update(self, backupset_name, backupset_description, default_backupset):
        """Updates the properties of the backupset.

            Args:
                backupset_name        (str)   --  new name of the backupset

                backupset_description (str)   --  description of the backupset

                default_backupset     (bool)  --  default backupset property

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

        request_json = {
            "association": {
                "entity": [{
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
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

        return self._process_update_reponse(request_json)

    @staticmethod
    def _get_epoch_time(timestamp):
        """Returns the Epoch time given the input time is in format %Y-%m-%d %H:%M:%S.

            Args:
                timestamp   (int / str)     --  value should either be the Epoch time or, the
                                                    Timestamp of the format %Y-%m-%d %H:%M:%S

            Returns:
                int - epoch time converted from the input timestamp

            Raises:
                SDKException:
                    if the input timestamp is not of correct format
        """
        if str(timestamp) == '0':
            return 0

        try:
            # return the timestamp value in int type
            return int(timestamp)
        except ValueError:
            # if not convertible to int, then convert the timestamp input to Epoch time
            try:
                return int(time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")))
            except Exception:
                raise SDKException('Subclient', '106')

    def _set_defaults(self, final_dict, defaults_dict):
        """Iterates over the defaults_dict, and adds the default value to the final_dict,
            for the key which is not present in the final dict.

            Recursively sets default values on the final_dict dictionary.

            Args:
                final_dict      (dict)  --  the dictionary to be set with defaults, and to be used
                                                to generate the Browse / Find JSON

                defaults_dict   (dict)  --  the dictionary with default values

            Returns:
                None
        """
        for key in defaults_dict:
            if key not in final_dict:
                final_dict[key] = defaults_dict[key]

            if isinstance(defaults_dict[key], dict):
                self._set_defaults(final_dict[key], defaults_dict[key])

    def _prepare_browse_options(self, options):
        """Prepares the options for the Browse/find operation.

            Args:
                options     (dict)  --  a dictionary of browse options

            Returns:
                dict - The browse options with all the default options set
        """
        self._set_defaults(options, self._default_browse_options)
        return options

    def _prepare_browse_json(self, options):
        """Prepares the JSON object for the browse request.

            Args:
                options     (dict)  --  the browse options dictionary

            Returns:
                dict - A JSON object for the browse response
        """
        operation_types = {
            'browse': 0,
            'find': 1,
            'all_versions': 2,
            'delete_data': 7
        }

        options['operation'] = options['operation'].lower()

        if options['operation'] not in operation_types:
            options['operation'] = 'find'

        # add the browse mode value here, if it is different for an agent
        # if agent is not added in the dict, default value 2 will be used
        browse_mode = {
            'virtual server': 4,
            'cloud apps': 3
        }

        mode = 2
        paths = []

        if isinstance(options['path'], basestring):
            paths.append(options['path'])
        elif isinstance(options['path'], list):
            paths = options['path']
        else:
            paths = ['\\']

        if self._agent_object.agent_name in browse_mode:
            mode = browse_mode[self._agent_object.agent_name]

        request_json = {
            "opType": operation_types[options['operation']],
            "mode": {
                "mode": mode
            },
            "paths": [{"path": path} for path in paths],
            "options": {
                "showDeletedFiles": options['show_deleted'],
                "restoreIndex": options['restore_index'],
                "vsDiskBrowse": options['vm_disk_browse'],
                "vsFileBrowse": options.get('vs_file_browse', False)
            },
            "entity": {
                "clientName": self._client_object.client_name,
                "clientId": int(self._client_object.client_id),
                "applicationId": int(self._agent_object.agent_id),
                "instanceId": int(self._instance_object.instance_id),
                "backupsetId": int(self.backupset_id),
                "subclientId": int(options['_subclient_id'])
            },
            "timeRange": {
                "fromTime": self._get_epoch_time(options['from_time']),
                "toTime": self._get_epoch_time(options['to_time'])
            },
            "advOptions": {
                "copyPrecedence": options['copy_precedence']
            },
            "ma": {
                "clientName": options['media_agent']
            },
            "queries": [{
                "type": 0,
                "queryId": "dataQuery",
                "dataParam": {
                    "sortParam": {
                        "ascending": False,
                        "sortBy": [0]
                    },
                    "paging": {
                        "pageSize": int(options['page_size']),
                        "skipNode": int(options['skip_node']),
                        "firstNode": 0
                    }
                }
            }]
        }

        if options['filters']:
            # [('FileName', '*.txt'), ('FileSize','GT','100')]
            request_json['queries'][0]['whereClause'] = []

            for browse_filter in options['filters']:
                if browse_filter[0] in ('FileName', 'FileSize'):
                    temp_dict = {
                        'connector': 0,
                        'criteria': {
                            'field': browse_filter[0],
                            'values': [browse_filter[1]]
                        }
                    }

                    if browse_filter[0] == 'FileSize':
                        temp_dict['criteria']['dataOperator'] = browse_filter[2]

                    request_json['queries'][0]['whereClause'].append(temp_dict)

        if options['job_id'] is not 0:
            request_json['advOptions']['advConfig'] = {
                'browseAdvancedConfigBrowseByJob': {
                    'commcellId': options['commcell_id'],
                    'jobId': options['job_id']
                }
            }

        if options['include_aged_data']:
            request_json['options']['includeAgedData'] = True

        if options['include_hidden']:
            request_json['options']['includeHidden'] = True

        if options['include_running_jobs']:
            request_json['options']['includeRunningJobs'] = True

        if options['vs_volume_browse']:
            request_json['mode']['mode'] = 3
            request_json['options']['vsVolumeBrowse'] = True
            request_json['advOptions']['browseViewName'] = options['browse_view_name']

        return request_json

    def _process_browse_all_versions_response(self, result_set):
        """Retrieves the items from browse response.

        Args:
            result_set  (dict)  --  browse response dict obtained from server

        Returns:
            dict - Dictionary of the specified file with list of all the file versions and
                    additional metadata retrieved from browse

        Raises:
            SDKException:
                if failed to browse/search for content

                if response is empty

                if response is not success
        """
        path = None
        versions_list = []

        for result in result_set:
            name = result['displayName']
            path = result['path']

            if 'modificationTime' in result:
                mod_time = time.localtime(result['modificationTime'])
                mod_time = time.strftime('%d/%m/%Y %H:%M:%S', mod_time)
            else:
                mod_time = None

            if 'file' in result['flags']:
                if result['flags']['file'] is True:
                    file_or_folder = 'File'
                else:
                    file_or_folder = 'Folder'
            else:
                file_or_folder = 'Folder'

            if 'size' in result:
                size = result['size']
            else:
                size = None

            if 'version' in result:
                version = result['version']
            else:
                version = None

            paths_dict = {
                'name': name,
                'version': version,
                'size': size,
                'modified_time': mod_time,
                'type': file_or_folder,
                'advanced_data': result['advancedData']
            }

            versions_list.append(paths_dict)

        all_versions_dict = dict()
        all_versions_dict[path] = versions_list

        return all_versions_dict

    def _process_browse_response(self, flag, response, options):
        """Retrieves the items from browse response.

        Args:
            flag        (bool)  --  boolean, whether the response was success or not

            response    (dict)  --  JSON response received for the request from the Server

            options     (dict)  --  The browse options dictionary

        Returns:
            list - List of only the file / folder paths from the browse response

            dict - Dictionary of all the paths with additional metadata retrieved from browse

        Raises:
            SDKException:
                if failed to browse/search for content

                if response is empty

                if response is not success
        """

        operation_types = {
            "browse": ('110', 'Failed to browse for subclient backup content\nError: "{0}"'),
            "find": ('111', 'Failed to Search\nError: "{0}"'),
            "all_versions": (
                '112', 'Failed to browse all version for specified content\nError: "{0}"'
            ),
            "delete_data": (
                '113', 'Failed to perform delete data operation for given content\nError: "{0}"'
            )
        }

        exception_code = operation_types[options['operation']][0]
        exception_message = operation_types[options['operation']][1]

        if flag:

            response_json = response.json()
            paths_dict = {}
            paths = []
            result_set = None
            browse_result = None

            # Send raw result as browse response for advanced use cases
            if options['_raw_response']:
                return [], response_json

            if response_json and 'browseResponses' in response_json:
                _browse_responses = response_json['browseResponses']
                for browse_response in _browse_responses:
                    if "browseResult" in browse_response:
                        browse_result = browse_response['browseResult']
                        if 'dataResultSet' in browse_result:
                            result_set = browse_result['dataResultSet']
                            break

                if not browse_result:
                    if 'messages' in response_json['browseResponses'][0]:
                        message = response_json['browseResponses'][0]['messages'][0]
                        error_message = message['errorMessage']

                        o_str = exception_message
                        raise SDKException('Subclient', '102', o_str.format(error_message))

                    else:
                        return [], {}

                if not result_set:
                    raise SDKException('Subclient', exception_code)

                if 'all_versions' in options['operation']:
                    return self._process_browse_all_versions_response(result_set)

                for result in result_set:
                    name = result.get('displayName')
                    snap_display_name = result.get('name')

                    if 'path' in result:
                        path = result['path']
                    else:
                        path = '\\'.join([options['path'], name])

                    if 'modificationTime' in result and result['modificationTime'] > 0:
                        mod_time = time.localtime(result['modificationTime'])
                        mod_time = time.strftime('%d/%m/%Y %H:%M:%S', mod_time)
                    else:
                        mod_time = None

                    if 'file' in result['flags']:
                        if result['flags']['file'] is True:
                            file_or_folder = 'File'
                        else:
                            file_or_folder = 'Folder'
                    else:
                        file_or_folder = 'Folder'

                    if 'size' in result:
                        size = result['size']
                    else:
                        size = None

                    paths_dict[path] = {
                        'name': name,
                        'snap_display_name': snap_display_name,
                        'size': size,
                        'modified_time': mod_time,
                        'type': file_or_folder,
                        'advanced_data': result['advancedData']
                    }

                    paths.append(path)

                return paths, paths_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _do_browse(self, options=None):
        """Performs a browse operation with the given options.

        Args:
            options     (dict)  --  dictionary of browse options

        Returns:
            list - List of only the file, folder paths from the browse response

            dict - Dictionary of all the paths with additional metadata retrieved from browse
        """
        if options is None:
            options = {}

        options = self._prepare_browse_options(options)
        request_json = self._prepare_browse_json(options)

        flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)

        return self._process_browse_response(flag, response, options)

    @property
    def name(self):
        """Returns the Backupset display name"""
        return self._properties["backupSetEntity"]["backupsetName"]

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

    @property
    def is_on_demand_backupset(self):
        """Treats the is on demand backupset as a read-only attribute."""
        return self._is_on_demand_backupset

    @property
    def plan(self):
        """Treats the backupset plan as a property of the Backupset class."""
        return self._plan

    @property
    def guid(self):
        """Treats the backupset GUID as a property of the Backupset class."""
        if self._properties.get('backupSetEntity'):
            if self._properties['backupSetEntity'].get('backupsetGUID'):
                return self._properties['backupSetEntity']['backupsetGUID']
            raise SDKException('Backupset', '102', 'Backupset GUID not found')
        raise SDKException('Backupset', '102', 'Backupset entity not found')

    @backupset_name.setter
    def backupset_name(self, value):
        """Sets the name of the backupset as the value provided as input.

            Raises:
                SDKException:
                    if failed to update the backupset name

                    if type of value input is not string
        """
        if isinstance(value, basestring):
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
            if isinstance(value, basestring):
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

    @plan.setter
    def plan(self, value):
        """Associates the plan to the backupset

            Raises:
                SDKException:

                    if input value is not an instance of Plan class

                    if plan does not exist

                    if plan associateion fails

                    if plan is not eligible to be associated
        """
        from .plan import Plan
        if isinstance(value, Plan):
            plan_obj = value
        elif isinstance(value, basestring):
            plan_obj = self._commcell_object.plans.get(value)
        else:
            raise SDKException('Backupset', '102', 'Input value is not of supported type')

        plans_obj = self._commcell_object.plans
        entity_dict = {
            'clientId': int(self._client_object.client_id),
            'appId': int(self._agent_object.agent_id),
            'backupsetId': int(self.backupset_id)
        }
        if plan_obj.plan_name in plans_obj.get_eligible_plans(entity_dict):
            request_json = {
                'backupsetProperties': {
                    'planEntity': {
                        'planSubtype': int(plan_obj.subtype),
                        '_type_': 158,
                        'planType': int(plan_obj.plan_type),
                        'planName': plan_obj.plan_name,
                        'planId': int(plan_obj.plan_id)
                    }
                }
            }

            response = self._process_update_reponse(
                request_json
            )

            if response[0]:
                return
            else:
                o_str = 'Failed to asspciate plan to the backupset\nError: "{0}"'
                raise SDKException('Backupset', '102', o_str.format(response[2]))
        else:
            raise SDKException(
                'Backupset',
                '102',
                'Plan not eligible to be associated with the backupset'
            )

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
        """Runs Incremental backup job for all subclients in this backupset.

            Runs Full Backup job for a subclient, if no job had been ran earlier for it.

            Returns:
                list    -   list consisting of the job objects for the backup jobs started for
                the subclients in the backupset

        """
        return_list = []
        thread_list = []

        if self.subclients.all_subclients:
            for subclient in self.subclients.all_subclients:
                thread = threading.Thread(
                    target=self._run_backup, args=(subclient, return_list)
                )
                thread_list.append(thread)
                thread.start()

        for thread in thread_list:
            thread.join()

        return return_list

    def browse(self, *args, **kwargs):
        """Browses the content of the Backupset.

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


            Refer `default_browse_options`_ for all the supported options.

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'browse'

        return self._do_browse(options)

    def find(self, *args, **kwargs):
        """Searches a file/folder in the backed up content of the backupset,
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


            Refer `default_browse_options`_ for all the supported options.

            Additional options supported:
                file_name       (str)   --  Find files with name

                file_size_gt    (int)   --  Find files with size greater than size

                file_size_lt    (int)   --  Find files with size lesser than size

                file_size_et    (int)   --  Find files with size equal to size

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'find'

        if 'path' not in options:
            options['path'] = '\\**\\*'

        if 'filters' not in options:
            options['filters'] = []

        if 'file_name' in options:
            options['filters'].append(('FileName', options['file_name']))

        if 'file_size_gt' in options:
            options['filters'].append(('FileSize', options['file_size_gt'], 'GTE'))

        if 'file_size_lt' in options:
            options['filters'].append(('FileSize', options['file_size_lt'], 'LTE'))

        if 'file_size_et' in options:
            options['filters'].append(('FileSize', options['file_size_et'], 'EQUALSBLAH'))

        return self._do_browse(options)

    def delete_data(self, paths):
        """Deletes items for the backupset in the Index and makes them unavailable for
        browsing and recovery

            Args:
                paths       (str/list)      --      The list of paths or single path to delete
                from the backupset

            Returns:
                None        --      If delete request is sent successfully

            Raises:
                Exception, if unable to prepare, response is invalid or send the
                delete data request

        """

        options = {
            'operation': 'delete_data',
            'path': paths
        }

        files, metadata = self._do_browse(options)

        # Delete operation does not return any result, hence consider the operation successful
        if files:
            raise SDKException('Backupset', '102', 'Delete data operation gave unexpected results')

    def refresh(self):
        """Refresh the properties of the Backupset."""
        self._get_backupset_properties()

        self.subclients = Subclients(self)
        self.schedules = Schedules(self)