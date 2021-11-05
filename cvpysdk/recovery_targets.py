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

from cvpysdk.exception import SDKException
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

            raise SDKException('RecoveryTarget', '102', 'No target exists with name: {0}'.format(recovery_target_name))

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

        self._policy_type = None
        self._application_type = None
        self._destination_hypervisor = None
        self._access_node = None
        self._users = []
        self._vm_prefix = ''
        self._vm_suffix = ''

        self._destination_host = None
        self._datastore = None
        self._resource_pool = None
        self._destination_network = None
        self._expiration_time = None
        self._failover_ma = None
        self._isolated_network = None
        self._no_of_cpu = None
        self._no_of_vm = None
        self._iso_paths = []

        self._resource_group = None
        self._region = None
        self._availability_zone = None
        self._storage_account = None
        self._vm_size = None
        self._disk_type = None
        self._virtual_network = None
        self._security_group = None
        self._create_public_ip = None
        self._restore_as_managed_vm = None
        self._test_virtual_network = None
        self._test_vm_size = None

        self._volume_type = None
        self._encryption_key = None
        self._instance_type = None

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
                self._application_type = self._recovery_target_properties['vmPolicyAppType']
                self._destination_hypervisor = self._recovery_target_properties['destinationHyperV']['clientName']
                vm_name_edit_string = self._recovery_target_properties.get('vmNameEditString')
                vm_name_edit_type = self._recovery_target_properties.get('vmNameEditType', 1)
                if vm_name_edit_string and vm_name_edit_type == 2:
                    self._vm_suffix = self._recovery_target_properties['vmNameEditString']
                elif vm_name_edit_string and vm_name_edit_type == 1:
                    self._vm_prefix = self._recovery_target_properties['vmNameEditString']
                self._access_node = self._recovery_target_properties['proxyClientEntity']['clientName']
                self._users = self._recovery_target_properties['securityAssociations']['users']
                self._policy_type = self._recovery_target_properties["entity"]["policyType"]

                if self._policy_type == 1:
                    self._availability_zone = (self._recovery_target_properties.get('amazonPolicy',{}).get('availabilityZones', [{}])[0].get('availabilityZoneName', None))
                    self._volume_type = self._recovery_target_properties.get('amazonPolicy', {}).get('volumeType', None)
                    # TODO: Encryption key support for SDK
                    self._encryption_key = None
                    self._destination_network = self._recovery_target_properties.get('networkList', [{}])[0].get('name', None)
                    self._security_group = self._recovery_target_properties.get('securityGroups', [{}])[0].get('name', '')
                    self._instance_type = (self._recovery_target_properties.get('amazonPolicy', {}).get('instanceType', [{}])[0].get('instanceType', {}).get('vmInstanceTypeName',''))
                    
                    expiry_hours = self._recovery_target_properties.get("minutesRetainUntil", None)
                    expiry_days = self._recovery_target_properties.get("daysRetainUntil", None)
                    if expiry_hours:
                        self._expiration_time = f'{expiry_hours} hours'
                    elif expiry_days:
                        self._expiration_time = f'{expiry_days} days'
                    self._test_virtual_network = self._recovery_target_properties.get('networkInfo', [{}])[0].get('label', None)
                    self._test_vm_size = (self._recovery_target_properties.get('amazonPolicy', {}).get('vmInstanceTypes', [{}])[0].get('vmInstanceTypeName',''))
                    
                elif self._policy_type == 2:
                    self._vm_folder = self._recovery_target_properties['dataStores'][0]['dataStoreName']
                    self._destination_network = self._recovery_target_properties['networkList'][0]['networkName']
                elif self._policy_type == 7:
                    self._resource_group = self._recovery_target_properties['esxServers'][0]['esxServerName']
                    self._region = self._recovery_target_properties['region']
                    self._availability_zone = (self._recovery_target_properties['amazonPolicy']
                                               ['availabilityZones'][0]['availabilityZoneName'])
                    self._storage_account = self._recovery_target_properties['dataStores'][0]['dataStoreName']

                    self._vm_size = (self._recovery_target_properties['amazonPolicy']['vmInstanceTypes']
                                     [0]['vmInstanceTypeName'])
                    self._disk_type = self._recovery_target_properties['amazonPolicy']['volumeType']
                    self._virtual_network = self._recovery_target_properties['networkList'][0]['networkDisplayName']
                    self._security_group = self._recovery_target_properties['securityGroups'][0]['name']
                    self._create_public_ip = self._recovery_target_properties['isPublicIPSettingsAllowed']
                    self._restore_as_managed_vm = self._recovery_target_properties['restoreAsManagedVM']

                    expiry_hours = self._recovery_target_properties.get("minutesRetainUntil")
                    expiry_days = self._recovery_target_properties.get("daysRetainUntil")
                    if expiry_hours:
                        self._expiration_time = f'{expiry_hours} hours'
                    elif expiry_days:
                        self._expiration_time = f'{expiry_days} days'
                    self._test_virtual_network = self._recovery_target_properties['networkInfo'][0]['label']
                    self._test_vm_size = (self._recovery_target_properties['amazonPolicy']['instanceType'][0]
                                          ['instanceType']['vmInstanceTypeName'])
                elif self._policy_type == 13:
                    self._destination_host = self._recovery_target_properties['esxServers'][0]['esxServerName']
                    self._datastore = self._recovery_target_properties['dataStores'][0]['dataStoreName']
                    self._resource_pool = self._recovery_target_properties['resourcePoolPath']
                    self._vm_folder = self._recovery_target_properties['folderPath']
                    self._destination_network = self._recovery_target_properties['networkList'][0]['destinationNetwork']

                    expiry_hours = self._recovery_target_properties.get("minutesRetainUntil")
                    expiry_days = self._recovery_target_properties.get("daysRetainUntil")
                    if expiry_hours:
                        self._expiration_time = f'{expiry_hours} hours'
                    elif expiry_days:
                        self._expiration_time = f'{expiry_days} days'
                    if self._recovery_target_properties.get('mediaAgent', {}):
                        self._failover_ma = self._recovery_target_properties['mediaAgent']['clientName']

                    self._isolated_network = self._recovery_target_properties.get("createIsolatedNetwork")

                    self._no_of_cpu = self._recovery_target_properties.get('maxCores')
                    self._no_of_vm = self._recovery_target_properties.get('maxVMQuota')
                    self._iso_paths = [iso['isoPath'] for iso in
                                       self._recovery_target_properties.get('isoInfo', [])]
                    if self._recovery_target_properties.get('associatedClientGroup'):
                        self._server_group = (self._recovery_target_properties["associatedClientGroup"]
                                              ["clientGroupName"])
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def recovery_target_id(self):
        """Returns: (str) the id of the recovery target"""
        return self._recovery_target_id

    @property
    def recovery_target_name(self):
        """Returns: (str) the display name of the recovery target"""
        return self._recovery_target_name

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
        """Returns: (str) the client name of the access node/proxy of the recovery target"""
        return self._access_node

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
    def destination_host(self):
        """Returns: (str) VMware: the destination ESX host name"""
        return self._destination_host

    @property
    def datastore(self):
        """Returns: (str) VMware: the datastore name"""
        return self._datastore

    @property
    def resource_pool(self):
        """Returns: (str) VMware: the resource pool name"""
        return self._resource_pool

    @property
    def vm_folder(self):
        """Returns: (str) VMware/Hyper-V: the destination VM folder"""
        return self._vm_folder

    @property
    def destination_network(self):
        """Returns: (str) VMware/Hyper-V/AWS: the network name of the destination VM"""
        return self._destination_network

    @property
    def expiration_time(self):
        """Returns: (str) VMware/Azure: the expiration time of the test boot VM/test failover VM
            eg: 4 hours or 3 days
        """
        return self._expiration_time

    @property
    def failover_ma(self):
        """Returns: (str) VMware: the preferred Media Agent to be used for test failover job"""
        return self._failover_ma

    @property
    def isolated_network(self):
        """Returns: (bool) VMware: whether the target is configured to create isolated network or not"""
        return self._isolated_network

    @property
    def iso_path(self):
        """Returns: list<str> VMware regular: the path of ISOs used for test boot operations"""
        return self._iso_paths

    @property
    def server_group(self):
        """Returns: (str) VMware regular: the name of the server group to be associated with the recovery target"""
        return self._server_group

    @property
    def no_of_cpu(self):
        """Returns: (str) VMware regular: the maximum number of CPU cores for live mount"""
        return self._no_of_cpu

    @property
    def no_of_vm(self):
        """Returns: (str) VMware regular: the maximum number of VMs to be deployed for live mount"""
        return self._no_of_vm

    @property
    def resource_group(self):
        """Returns: (str) Azure: the resource group name for destination VM"""
        return self._resource_group

    @property
    def region(self):
        """Return: (str) Azure: the recovery target region for destination VM"""
        return self._region

    @property
    def availability_zone(self):
        """Return: (str) Azure/AWS: the availability zone of the destination VM"""
        return self._availability_zone

    @property
    def storage_account(self):
        """Returns: (str) Azure: the storage account name used to deploy the VM's storage"""
        return self._storage_account

    @property
    def vm_size(self):
        """Returns: (str) Azure: the size of the destination VM. This defines the hardware config"""
        return self._vm_size

    @property
    def disk_type(self):
        """Returns: (str) Azure: the disk type of the destination VM"""
        return self._disk_type

    @property
    def virtual_network(self):
        """Returns: (str) Azure: the destination VM virtual network to assign NIC to"""
        return self._virtual_network

    @property
    def security_group(self):
        """Returns: (str) Azure/AWS: the destination VM network security group name"""
        return self._security_group

    @property
    def create_public_ip(self):
        """Returns: (bool) Azure: whether public IP will be created for destination VM"""
        return self._create_public_ip

    @property
    def restore_as_managed_vm(self):
        """Returns: (bool) whether the destination VM will be a managed VM"""
        return self._restore_as_managed_vm

    @property
    def test_virtual_network(self):
        """Returns: (str) Azure: the destination VM virtual network for test failover"""
        return self._test_virtual_network

    @property
    def test_vm_size(self):
        """Returns: (str) Azure: the destination VM size for test failover"""
        return self._test_vm_size

    @property
    def volume_type(self):
        """Returns: (str) AWS: the destination VM volume type/disk type"""
        return self._volume_type

    @property
    def encryption_key(self):
        """Returns: (str) AWS: the encryption key of the destination VM. Not implemented"""
        return self._encryption_key

    @property
    def instance_type(self):
        """Returns: (str) AWS: the AWS instance type which is used for defining hardware config"""
        return self._instance_type

    def refresh(self):
        """Refresh the properties of the Recovery Target."""
        self._get_recovery_target_properties()
