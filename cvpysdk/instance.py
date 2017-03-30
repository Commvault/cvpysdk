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

"""

from __future__ import absolute_import

from .subclient import Subclients
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

        self._INSTANCES = self._commcell_object._services.GET_ALL_INSTANCES % (
            self._agent_object._client_object.client_id
        )

        self._instances = self._get_instances()

        from .instances.vsinstance import VirtualServerInstance
        from .instances.cainstance import CloudAppsInstance

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        self._instances_dict = {
            'virtual server': VirtualServerInstance,
            'cloud apps': CloudAppsInstance
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

                        agent = str(dictionary['instance']['appName']).lower()

                        if self._agent_object.agent_name in agent:
                            temp_name = str(dictionary['instance']['instanceName']).lower()
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
        if not isinstance(instance_name, str):
            raise SDKException('Instance', '101')

        return self._instances and str(instance_name).lower() in self._instances

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
        if not isinstance(instance_name, str):
            raise SDKException('Instance', '101')
        else:
            instance_name = str(instance_name).lower()

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
                object - instance of the Backupset class
        """
        from .backupset import Backupsets

        self._agent_object = agent_object
        self._commcell_object = self._agent_object._commcell_object

        self._instance_name = str(instance_name).lower()

        if instance_id:
            # Use the instance id provided in the arguments
            self._instance_id = str(instance_id)
        else:
            # Get the id associated with this instance
            self._instance_id = self._get_instance_id()

        self._INSTANCE = self._commcell_object._services.INSTANCE % (self.instance_id)

        self._properties = None

        self._get_instance_properties()

        self.backupsets = Backupsets(self)
        self.subclients = Subclients(self)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Instance class instance for Instance: "{0}" of Agent: "{1}"'
        return representation_string.format(self.instance_name, self._agent_object.agent_name)

    def _get_instance_id(self):
        """Gets the instance id associated with this backupset.

            Returns:
                str - id associated with this instance
        """
        instances = Instances(self._agent_object)
        return instances.get(self.instance_name).instance_id

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

                instance_name = self._properties["instance"]["instanceName"]
                self._instance_name = str(instance_name).lower()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def instance_id(self):
        """Treats the instance id as a read-only attribute."""
        return self._instance_id

    @property
    def instance_name(self):
        """Treats the instance name as a read-only attribute."""
        return self._instance_name
