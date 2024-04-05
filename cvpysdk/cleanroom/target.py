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

"""Main file for performing Cleanroom Target specific operations.

CleanroomTargets and CleanroomTarget are 2 classes defined in this file.

CleanroomTargets:     Class for representing all the cleanroom targets

CleanroomTarget:      Class for a single cleanroom target selected, and to perform operations on that cleanroom target


cleanroomTargets:
    __init__()                   --  initialize object of CleanroomTargets class

    __str__()                   --  returns all the Cleanroom Targets

    _get_cleanroom_targets()     -- Gets all the cleanroom targets

    has_cleanroom_target()       -- Checks if a target is present in the commcell.

    get()                        --  returns the cleanroom target class object of the input target name

    refresh()                   --  refresh the targets present in the client

cleanroomTargets Attributes
--------------------------

    **all_targets**             --  returns the dictionary consisting of all the targets that are
    present in the commcell and their information such as id and name

CleanroomTarget:
    __init__()                   --   initialize object of CleanroomTarget with the specified cleanroom target name

    _get_cleanroom_target_id()   --   method to get the cleanroom target id

    _get_cleanroom_target_properties()  --   get the properties of this recovery target

    _delete_cleanroom_target()    -- Deletes the cleanroom target

    delete()                     -- Deletes the cleanroom target

    refresh()                   --   refresh the object properties

CleanroomTarget Attributes
--------------------------

    **cleanroom_target_id**      -- Returns the id of the cleanroom target
    **cleanroom_target_name**    -- Returns the name of the cleanroom Target
    **destination_hypervisor**  -- Returns the name of destination hypervisor
    **vm_prefix**               -- Returns the prefix of the vm name
    **destination_host**        -- Returns the destination host
    **storage_account**          -- Returns the storage_account host
    **policy_type**             -- Returns the policy type
    **application_type**          -- Returns the application type
    **restore_as_managed_vm**   -- Returns the restore_as_managed_vm
    **region**                  -- Returns the region
    **expiration_time**         -- Returns the _expiration_time
    **vm_suffix**               -- Returns the vm_suffix
    **vm_prefix**               -- Returns the vm_prefix
    **access_node**             -- Returns the access_node
    **access_node_client_group** -- Returns the access_node_client_group

"""
from __future__ import absolute_import
from __future__ import unicode_literals

from cvpysdk.exception import SDKException


class CleanroomTargets:

    """Class for representing all the Cleanroom targets"""

    def __init__(self, commcell_object):
        """Initialize object of the CleanroomTargets class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._RECOVERY_TARGETS_API = self._services['GET_ALL_RECOVERY_TARGETS']

        self._cleanroom_targets = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all targets .

            Returns:
                str     -   string of all the targets

        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'CleanroomTargets')

        for index, cleanroom_target in enumerate(self._cleanroom_targets):
            sub_str = '{:^5}\t{:20}\n'.format(
                index + 1,
                cleanroom_target
            )
            representation_string += sub_str

        return representation_string.strip()

    def _get_cleanroom_targets(self):
        """Gets all the cleanroom targets.

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
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGETS_API)
        if flag:
            if response.json() and 'recoveryTargets' in response.json():
                cleanroom_target_dict = {}
                for cleanroomTarget in response.json()['recoveryTargets']:
                    if cleanroomTarget['applicationType'] == "CLEAN_ROOM":
                        temp_name = cleanroomTarget['name'].lower()
                        cleanroom_target_dict[temp_name] = str(cleanroomTarget['id'])

                return cleanroom_target_dict
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
        return self._cleanroom_targets

    def has_cleanroom_target(self, target_name):
        """Checks if a target is present in the commcell.

            Args:
                target_name (str)  --  name of the target

            Returns:
                bool - boolean output whether the target is present in commcell or not

            Raises:
                SDKException:
                    if type of the target name argument is not string

        """
        if not isinstance(target_name, str):
            raise SDKException('Target', '101')

        return self._cleanroom_targets and target_name.lower() in self._cleanroom_targets

    def get(self, cleanroom_target_name):
        """Returns a target object.

            Args:
                cleanroom_target_name (str)  --  name of the target

            Returns:
                object - instance of the target class for the given target name

            Raises:
                SDKException:
                    if type of the target name argument is not string

                    if no target exists with the given name

        """
        if not isinstance(cleanroom_target_name, str):
            raise SDKException('Target', '101')
        else:
            cleanroom_target_name = cleanroom_target_name.lower()

            if self.has_cleanroom_target(cleanroom_target_name):
                return CleanroomTarget(
                    self._commcell_object, cleanroom_target_name, self.all_targets[cleanroom_target_name])

            raise SDKException('RecoveryTarget', '102', 'No target exists with name: {0}'.format(cleanroom_target_name))

    def refresh(self):
        """Refresh the cleanroom targets"""
        self._cleanroom_targets = self._get_cleanroom_targets()


class CleanroomTarget:
    """Class for performing target operations"""

    def __init__(self, commcell_object, cleanroom_target_name, cleanroom_target_id=None):
        """Initialize the instance of the CleanroomTarget class.

            Args:
                commcell_object   (object)    --  instance of the Commcell class

                cleanroom_target_name      (str)       --  name of the target

                cleanroom_target_id        (str)       --  id of the target

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._cleanroom_target_name = cleanroom_target_name.lower()

        if cleanroom_target_id:
            # Use the target id mentioned in the arguments
            self._cleanroom_target_id = str(cleanroom_target_id)
        else:
            # Get the target id if target id is not provided
            self._cleanroom_target_id = self._get_cleanroom_target_id()
        self._RECOVERY_TARGET_API = self._services['GET_RECOVERY_TARGET'] % self._cleanroom_target_id

        self._cleanroom_target_properties = None

        self._policy_type = None
        self._application_type = None
        self._destination_hypervisor = None
        self._access_node = None
        self._access_node_client_group = None
        self._users = []
        self._user_groups = []
        self._vm_prefix = ''
        self._vm_suffix = ''
        self._expiration_time = None

        self._region = None
        self._availability_zone = None
        self._storage_account = None
        self._restore_as_managed_vm = None

        self.refresh()

    def _get_cleanroom_target_id(self):
        """Gets the target id associated with this target.

            Returns:
                str - id associated with this target

        """
        target = CleanroomTargets(self._commcell_object)
        return target.all_targets[self._cleanroom_target_name]

    def _delete_cleanroom_target(self):
        """Deletes the cleanroom target

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('DELETE', self._RECOVERY_TARGET_API)
        if flag:
            return flag
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_policy_type(self, policy_type):
        """Sets the policy type"""
        if policy_type == "AMAZON":
            self._policy_type = 1
        elif policy_type == "MICROSOFT":
            self._policy_type = 2
        elif policy_type == "AZURE_RESOURCE_MANAGER":
            self._policy_type = 7
        elif policy_type in ["VMW_BACKUP_LABTEMPLATE", "VMW_LIVEMOUNT"]:
            self._policy_type = 13
        else:
            self._policy_type = -1

    def _get_cleanroom_target_properties(self):
        """Gets the target properties of this target.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGET_API)

        if flag:
            if response.json() and 'entity' in response.json():
                self._cleanroom_target_properties = response.json()
                self._application_type = self._cleanroom_target_properties['entity']['applicationType']
                self._destination_hypervisor = self._cleanroom_target_properties['entity']['destinationHypervisor'][
                    'name']
                self._vm_suffix = self._cleanroom_target_properties["vmDisplayName"].get("suffix", "")
                self._vm_prefix = self._cleanroom_target_properties["vmDisplayName"].get("prefix", "")
                self._access_node = self._cleanroom_target_properties["accessNode"].get("type", "")
                self._access_node_client_group = (self._cleanroom_target_properties.get('proxyClientGroupEntity', {})
                                                  .get('clientGroupName'))
                self._users = self._cleanroom_target_properties.get('securityOptions', {}).get('users', [])
                self._user_groups = self._cleanroom_target_properties.get('securityOptions', {}).get('userGroups', [])
                policy_type = self._cleanroom_target_properties["entity"].get("policyType", "")
                self._set_policy_type(policy_type)

                if self._policy_type == 7:
                    self._region = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                    .get('region', {})
                                    .get('name'))
                    self._availability_zone = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                               .get('availabilityZone'))
                    self._storage_account = (self._cleanroom_target_properties.get("destinationOptions", {})
                                             .get("dataStore", ""))

                    self._vm_size = (self._cleanroom_target_properties.get('amazonPolicy', {})
                                     .get('vmInstanceTypes', [{}])[0]
                                     .get('vmInstanceTypeName', ''))
                    self._disk_type = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                       .get('volumeType'))
                    self._virtual_network = (self._cleanroom_target_properties.get('networkOptions', {})
                                             .get('networkCard', {})
                                             .get('networkDisplayName'))
                    self._security_group = (self._cleanroom_target_properties.get('securityOptions', {})
                                            .get('securityGroups', [{}])[0]
                                            .get('name', ''))
                    self._create_public_ip = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                              .get('publicIP'))
                    self._restore_as_managed_vm = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                                   .get('restoreAsManagedVM'))
                    expiry_hours = (self._cleanroom_target_properties.get("liveMountOptions", {})
                                    .get("expirationTime", {})
                                    .get("minutesRetainUntil", ""))
                    expiry_days = (self._cleanroom_target_properties.get("liveMountOptions", {})
                                   .get("expirationTime", {})
                                   .get("daysRetainUntil", ""))
                    if expiry_hours:
                        self._expiration_time = f'{expiry_hours} hours'
                    elif expiry_days:
                        self._expiration_time = f'{expiry_days} days'
                    self._test_virtual_network = (self._cleanroom_target_properties.get('networkOptions', {})
                                                  .get('cloudNetwork', {})
                                                  .get('label'))
                    self._test_vm_size = (self._cleanroom_target_properties.get('amazonPolicy', {})
                                          .get('vmInstanceTypes', [{}])[0]
                                          .get('vmInstanceTypeName', ''))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def cleanroom_target_id(self):
        """Returns: (str) the id of the cleanroom target"""
        return self._cleanroom_target_id

    @property
    def cleanroom_target_name(self):
        """Returns: (str) the display name of the cleanroom target"""
        return self._cleanroom_target_name

    @property
    def policy_type(self):
        """Returns: (str) the policy type ID
            1  - AWS
            2  - Microsoft Hyper-V
            7  - Azure
            13 - VMware
        """
        return self._policy_type

    @property
    def application_type(self):
        """Returns: (str) the name of the application type
            0 - Replication type
            1 - Regular type
        """
        return self._application_type

    @property
    def destination_hypervisor(self):
        """Returns: (str) the client name of destination hypervisor"""
        return self._destination_hypervisor

    @property
    def access_node(self):
        """Returns: (str) the client name of the access node/proxy of the cleanroom target"""
        return self._access_node

    @property
    def access_node_client_group(self):
        """Returns: (str) The client group name set on the access node field of cleanroom target"""
        return self._access_node_client_group

    @property
    def security_user_names(self):
        """Returns: list<str> the names of the users who are used for ownership of the hypervisor and VMs"""
        return [user['userName'] for user in self._users]

    @property
    def vm_prefix(self):
        """Returns: (str) the prefix of the vm name to be prefixed to the destination VM"""
        return self._vm_prefix

    @property
    def vm_suffix(self):
        """Returns: (str) the suffix of the vm name to be suffixed to the destination VM"""
        return self._vm_suffix

    @property
    def expiration_time(self):
        """Returns: (str) VMware/Azure: the expiration time of the test boot VM/test failover VM
            eg: 4 hours or 3 days
        """
        return self._expiration_time

    @property
    def storage_account(self):
        """Returns: (str) Azure: the storage account name used to deploy the VM's storage"""
        return self._storage_account

    @property
    def region(self):
        """Return: (str) Azure: the cleanroom target region for destination VM"""
        return self._region

    @property
    def restore_as_managed_vm(self):
        """Returns: (bool) whether the destination VM will be a managed VM"""
        return self._restore_as_managed_vm

    def refresh(self):
        """Refresh the properties of the cleanroom Target."""
        self._get_cleanroom_target_properties()

    def delete(self):
        """Deletes the Cleanroom Target. Returns: (bool) whether the target is deleted or not."""
        return self._delete_cleanroom_target()
