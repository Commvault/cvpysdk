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

"""Main file for performing Recovery Target specific operations.

RecoveryTargets and RecoveryTarget are 2 classes defined in this file.

RecoveryTargets:     Class for representing all the recovery targets

RecoveryTarget:      Class for a single recovery target selected, and to perform operations on that recovery target


RecoveryTargets:
    __init__()                   --  initialize object of RecoveryTargets class

    __str__()                   --  returns all the Recovery Targets

    _get_recovery_targets()     -- Gets all the recovery targets

    has_recovery_target()       -- Checks if a target is present in the commcell.

    get()                        --  returns the recovery target class object of the input target name

    refresh()                   --  refresh the targets present in the client

RecoveryTargets Attributes
--------------------------

    **all_targets**             --  returns the dictioanry consisting of all the targets that are
    present in the commcell and their information such as id and name

RecoveryTarget:
    __init__()                   --   initialize object of RecoveryTarget with the specified recovery target name

    _get_recovery_target_id()   --   method to get the recovery target id

    _get_recovery_target_properties()  --   get the properties of this ecovery target

    refresh()                   --   refresh the object properties

RecoveryTarget Attributes
--------------------------

    **recovery_target_id**      -- Returns the id of the recovery target
    **recovery_target_name**    -- Returns the name of the Recovery Target
    **destination_hypervisor**  -- Returns the name of destination hypervisor
    **vm_prefix**               -- Returns the prefix of the vm name
    **destination_host**        -- Returns the destination host
    ** def datastore**          -- Returns the datastore host
    **resource_pool**           -- Returns the resource_pool host
    **destination_network**     -- Returns the destination_network host
    **no_of_cpu**               -- Returns the no_of_cpu host
    **no_of_vm**                -- Returns the no_of_vm hos

"""
from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring


class RecoveryTargets:

    """Class for representing all the clients associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Clients class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._RECOVERY_TARGETS = self._services['GET_ALL_RECOVERY_TARGETS']

        self._recovery_targets = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all targets .

            Returns:
                str     -   string of all the targets

        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'RecoverTargets')

        for index, recovery_target in enumerate(self._recovery_targets):
            sub_str = '{:^5}\t{:20}\n'.format(
                index + 1,
                recovery_target
            )
            representation_string += sub_str

        return representation_string.strip()


    def _get_recovery_targets(self):
        """Gets all the recovery targets.

            Returns:
                dict - consists of all targets in the client
                    {
                         "target1_name": target1_id,
                         "target2_name": target2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGETS)

        if flag:
            if response.json() and 'policy' in response.json():

                recovery_target_dict = {}

                for dictionary in response.json()['policy']:
                    temp_name = dictionary['entity']['vmAllocPolicyName'].lower()
                    recovery_target_dict[temp_name] = str(dictionary['entity']['vmAllocPolicyId'])

                return recovery_target_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_targets(self):
        """Returns dict of all the targets.

         Returns dict    -   consists of all targets

                {
                    "target1_name": target1_id,

                    "target2_name": target2_id
                }

        """
        return self._recovery_targets

    def has_recovery_target(self, target_name):
        """Checks if a target is present in the commcell.

            Args:
                target_name (str)  --  name of the target

            Returns:
                bool - boolean output whether the target is present in commcell or not

            Raises:
                SDKException:
                    if type of the target name argument is not string

        """
        if not isinstance(target_name, basestring):
            raise SDKException('Target', '101')

        return self._recovery_targets and target_name.lower() in self._recovery_targets

    def get(self, recovery_target_name):
        """Returns a target object.

            Args:
                target_name (str)  --  name of the target

            Returns:
                object - instance of the target class for the given target name

            Raises:
                SDKException:
                    if type of the target name argument is not string

                    if no target exists with the given name

        """
        if not isinstance(recovery_target_name, basestring):
            raise SDKException('Target', '101')
        else:
            recovery_target_name = recovery_target_name.lower()

            if self.has_recovery_target(recovery_target_name):
                return RecoveryTarget(
                    self._commcell_object, recovery_target_name, self.all_targets[recovery_target_name])

            raise SDKException('RecoveryTarget', '102', 'No target exists with name: {0}'.format(target_name))

    def refresh(self):
        """Refresh the recovery targets"""
        self._recovery_targets = self._get_recovery_targets()


class RecoveryTarget:

    """Class for performing target operations"""

    def __init__(self, commcell_object, recovery_target_name, recovery_target_id=None):
        """Initialize the instance of the RecoveryTarget class.

            Args:
                commcell_object   (object)    --  instance of the Commcell class

                target_name      (str)       --  name of the target

                target_id        (str)       --  id of the target

                    default: None

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._recovery_target_name = recovery_target_name.lower()

        if recovery_target_id:
            # Use the target id mentioned in the arguments
            self._recovery_target_id = str(recovery_target_id)
        else:
            # Get the target id if target id is not provided
            self._recovery_target_id = self._get_recovery_target_id()
        self._RECOVERY_TARGET = self._services['GET_RECOVERY_TARGET'] %(self._recovery_target_id)

        self._recovery_target_properties = None

        self._destination_hypervisor = None
        self._vm_prefix = ''
        self._destination_host = None
        self._datastore = None
        self._resource_pool = None
        self._destination_network = None
        self._no_of_cpu = None
        self._no_of_vm = None
        self.refresh()

    def _get_recovery_target_id(self):
        """Gets the target id associated with this target.

            Returns:
                str - id associated with this target

        """
        target = RecoveryTargets(self._commcell_object)
        return target.get(self._recovery_target_name)

    def _get_recovery_target_properties(self):
        """Gets the target properties of this target.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGET)

        if flag:
            if response.json() and 'policy' in response.json():
                self._recovery_target_properties = response.json()['policy'][0]
                self._destination_hypervisor = self._recovery_target_properties['destinationHyperV']['clientName']
                if 'vmNameEditString' in self._recovery_target_properties.keys():
                    self._vm_prefix = self._recovery_target_properties['vmNameEditString']
                self._destination_host = self._recovery_target_properties['esxServers'][0]['esxServerName']
                self._datastore = self._recovery_target_properties['dataStores'][0]['dataStoreName']
                self._resource_pool = self._recovery_target_properties['resourcePoolPath']
                self._destination_network = self._recovery_target_properties['networkList'][0]['destinationNetwork']
                self._no_of_cpu = self._recovery_target_properties['maxCores']
                self._no_of_vm = self._recovery_target_properties['maxVMQuota']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def recovery_target_id(self):
        """Returns the id of the recovery target."""
        return self._recovery_target_id

    @property
    def recovery_target_name(self):
        """Returns the name of the Recovery Target."""
        return self._recovery_target_name

    @property
    def destination_hypervisor(self):
        """Returns the name of destination hypervisor"""
        return self._destination_hypervisor

    @property
    def vm_prefix(self):
        """Returns the prefix of the vm name"""
        return self._vm_prefix

    @property
    def destination_host(self):
        """Returns the destination host"""
        return self._destination_host

    @property
    def datastore(self):
        """Returns the datastore host"""
        return self._datastore

    @property
    def resource_pool(self):
        """Returns the resource_pool host"""
        return self._resource_pool

    @property
    def destination_network(self):
        """Returns the destination_network host"""
        return self._destination_network

    @property
    def no_of_cpu(self):
        """Returns the no_of_cpu host"""
        return self._no_of_cpu

    @property
    def no_of_vm(self):
        """Returns the no_of_vm host"""
        return self._no_of_vm

    def refresh(self):
        """Refresh the properties of the Recovery Target."""
        self._get_recovery_target_properties()
