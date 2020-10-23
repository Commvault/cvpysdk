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

"""Main file for performing virtual machine policy related operations on the Commcell.

VirtualMachinePolicies:         Class for representing all the Virtual Machine Policies associated
                                    with the Commcell

VirtualMachinePolicy:           Class for representing a single Virtual Machine Policy. Contains
                                    method definitions for common methods among all VM Policies

LiveMountPolicy:                Class for representing a single Live Mount Policy associated with
                                    the Commcell; inherits VirtualMachinePolicy


VirtualMachinePolicies:
    __init__(commcell_object)               --  initialize the VirtualMachinePolicies instance for
                                                    the Commcell

    __str__()                               --  returns all the Virtual Machine policies associated
                                                    with the Commcell

    __repr__()                              --  returns a string for the instance of the
                                                    VirtualMachinePolicies class

    _get_vm_policies()                      --  gets all the Virtual Machine policies of the
                                                    Commcell

    _set_vclient_and_vcenter_names()        --  sets the virtualization client name; if a
                                                    vclient name is passed, checks against the
                                                    available virtualization clients, otherwise
                                                    sets the first one in the lists the vclient

    _prepare_add_vmpolicy_json_default
                    (vm_policy_options)     --  sets values for creating the add policy json
                                                    that are common across all vm policies

    _get_data_center_json
                    (vm_policy_options)     --  sets values for creating the datacenter json value
                                                    in the add policy json

    _set_data_center(vm_policy_options)     --  sets the datacenter name if provided by user, or
                                                    sets the alphabetically lowest one in the
                                                    vcenter as default

    _get_esx_servers_json
                    (vm_policy_options)     --  sets values for creating the esxServers value in
                                                    the add policy json

    _get_esx_server_list(_datacenter)       --  returns list of esx servers in the datacenter

    _get_data_stores_json
                (vm_policy_options)         --  sets values for creating the datastore value in the
                                                    add policy json

    _get_datastores_list(_esxservers)       --  returns list of datastores for all the esx servers
                                                    that are specified

    _clone_vm_policy(vm_policy_json)        --  private method to clone a vm policy from
                                                    VirtualMachinePolicy object

    _prepare_add_vmpolicy_json_livemount
                     (vm_policy_options)    --  sets values for creating the add policy json that
                                                    are specific for creating Live Mount policy

    _security_associations_json
                    (vm_policy_options)     --  sets values for creating the security associations
                                                    value in the add policy json

    _network_names_json
                (vm_policy_options)         --  sets values for creating the network names value in
                                                    the add policy json

    _media_agent_json(vm_policy_options)    --  sets values for creating the media agent json
                                                    value in the add policy json (only for
                                                    Live Mount policy)

    _entity_json(vm_policy_options)         --  sets values for creating the entity json value in
                                                    the add policy json

    has_policy(vm_policy_name)              --  checks if a Virtual Machine policy exists with the
                                                    given name in a particular instance

    get(vm_policy_name)                     --  returns a VirtualMachinePolicy object of the
                                                    specified virtual machine policy name

    add(vm_policy_name, vm_policy_type,
        vclient_name, vm_policy_options)    --  adds a new Virtual Machine policy to the
                                                    VirtualMachinePolicies instance,and returns an
                                                    object of corresponding vm_policy_type

    delete(vm_policy_name)                  --  removes the specified Virtual Machine policy from
                                                    the Commcell

    refresh()                               --  refresh the virtual machine policies


VirtualMachinePolicy:
    __new__(
            cls,
            commcell_object,
            vm_policy_name,
            vm_policy_type_id,
            vm_policy_id=None)                    --  decides which instance object needs to be
                                                          created

    __init__(commcell_object,
             vm_policy_name,
             vm_policy_type,
             VMPolicy_id,
             vm_policy_details)                   --  initialize the instance of
                                                          VirtualMachinePolicy class for a specific
                                                          virtual machine policy of the Commcell

    __repr__()                                    --  returns a string representation of the
                                                          VirtualMachinePolicy instance

    _get_vm_policy_id()                           --  gets the id of the vm policy

    _get_vm_policy_properties()                  --  returns the  policy properties

    _update_vm_policy()                           --  updates the vm policy using a PUT request
                                                          with the updated properties json.

    disable(vm_policy_name)                       --  disables the specified policy, if enabled

    enable(vm_policy_name)                        --  enables the specified policy, if disabled

    clone(desired_vm_policy_name)                 --  copies properties of the vm policy instance
                                                          and creates a new VM Policy with the
                                                          specified name

    properties()                                  --  returns the properties of the vm policy as a
                                                          dictionary

    refresh()                                     --  refresh the virtual machine policy properties

LiveMountPolicy:
    __init__(commcell_object,
             vm_policy_name,
             vm_policy_type,
             VMPolicy_id,
             vm_policy_details)                     --  initialize the instance of LiveMountPolicy
                                                            class for a specific virtual machine
                                                            policy of the Commcell

    __repr__()                                      --  returns a string representation of the
                                                            LiveMountPolicy instance

    _set_mounted_vm_name(live_mount_options)        --  sets the vm name for the live mounted vm

    _prepare_live_mount_json(live_mount_options)    --  sets values for creating the add policy
                                                            json

    __associations_json(live_mount_options)         --  sets the associations value for the live
                                                            mount job json

    _task_json(live_mount_options)                  --  sets the task value for the live mount job
                                                            json

    _subtask_json(live_mount_options)               --  sets the subTask value for the live mount
                                                            job json

    _one_touch_response_json(live_mount_options)    --  sets the oneTouchResponse value for the
                                                            live mount job json

    _hwconfig_json(live_mount_options)              --  sets the hwConfig value for the live mount
                                                            job json

    _netconfig_json(live_mount_options)             --  sets the netConfig value for the live mount
                                                            job json

    _vm_entity_json(live_mount_options)             --  sets the vmEntity value for the live mount
                                                            job json

    _vm_info_json(live_mount_options)               --  Sets the vmInfo value for the live mount
                                                            job json

    _is_hidden_client(self, client_name)            --  checks if specified client is a hidden
                                                            client for the Commcell instance

    _validate_live_mount(self, client_name)         --  check if the specified vm has a backup
                                                            for live mount

    view_active_mounts()                            --  shows all active mounts for the specified
                                                            Live Mount Policy instance

    live_mount(vm_name,
                live_mount_options=None)            --  run Live Mount for this Live Mount policy
                                                            instance
"""

from __future__ import unicode_literals

from past.builtins import basestring

from .exception import SDKException
from .job import Job


class VirtualMachinePolicies(object):
    """Class for representing all the Virtual Machine Policies associated with the Commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the VirtualMachinePolicies class.

            Args:
                commcell_object (object)  --  instance of the Commcell class
            Returns:
                object - instance of the VirtualMachinePolicies class
        """
        self._commcell_object = commcell_object

        self._VMPOLICIES_URL = self._commcell_object._services['VM_ALLOCATION_POLICY']
        self._ALL_VMPOLICIES_URL = self._commcell_object._services['ALL_VM_ALLOCATION_POLICY']
        self._VCLIENTS_URL = self._commcell_object._services['GET_VIRTUAL_CLIENTS']
        self._QOPERATION_URL = self._commcell_object._services['EXECUTE_QCOMMAND']

        self._vm_policies = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all virtual machine policies of the commcell.

            Returns:
                str - string of all the virtual machine policies associated with the commcell
        """
        representation_string = '{:^5}\t{:^28}'.format('S. No.', 'Virtual Machine Policy')

        for (index, vm_policy) in enumerate(self._vm_policies):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, vm_policy)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Clients class."""
        return "VirtualMachinePolicies class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name)

    def _get_vm_policies(self):
        """Gets all the virtual machine policies associated to the commcell specified by the
            Commcell object.

            Returns:
                dict - consists of all virtual machine policies for the commcell
                    {
                        "vm_policy1_name": {
                                                "id": vm_policy1Id,
                                                "policyType": policyTypeId
                                            }
                        "vm_policy2_name": {
                                                "id": vm_policy2Id,
                                                "policyType": policyTypeId
                                            }
                    }
            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='GET', url=self._ALL_VMPOLICIES_URL)

        if flag:
            if response.json() and 'policy' in response.json():
                vm_policies = response.json()['policy']

                if vm_policies == []:
                    return {}

                vm_policies_dict = {}

                for vm_policy in vm_policies:
                    temp_name = vm_policy['entity']['vmAllocPolicyName'].lower()
                    temp_id = str(vm_policy['entity']['vmAllocPolicyId']).lower()
                    temp_policy_type = str(vm_policy['entity']['policyType']).lower()
                    vm_policies_dict[temp_name] = {
                        'id': temp_id,
                        'policyType': temp_policy_type
                    }

                return vm_policies_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _set_vclient_and_vcenter_names(self, vm_policy_options, vclient_name):
        """Sets the virtualization client name and the vcenter name for the corresponding vclient

            Args:
                vm_policy_options    --  optional policy paramters passed by user (None if user
                                             passes nothing

                vclient_name         --  virtualization client name

            Raises:
                SDKException:
                    if response is not success

                    if no virtualization client exists on the Commcell

                    if virtualization client with given name does not exist on this Commcell
        """
        clients = self._commcell_object.clients
        vclient_name_dict = clients._get_virtualization_clients()

        if not vclient_name_dict:
            err_msg = 'No virtualization clients exist on this Commcell.'
            raise SDKException('Virtual Machine', '102', err_msg)

        if vclient_name in vclient_name_dict:
            vm_policy_options['clientName'] = vclient_name
            # fetching the vcenter from the corresponding instance object
            client = self._commcell_object.clients.get(vm_policy_options['clientName'])
            agent = client.agents.get('Virtual Server')
            instance_keys = next(iter(agent.instances._instances))
            instance = agent.instances.get(instance_keys)
            vm_policy_options['vCenterName'] = instance.server_host_name[0]
        else:
            err_msg = 'Virtualization client "{0}" does not exist'.format(vclient_name)
            raise SDKException('Virtual Machine', '102', err_msg)

    def _get_proxy_client_json(self, options):
        try:
            id_ = self._commcell_object.clients[options.get("proxy_client")]["id"]
        except KeyError:
            return dict()
        return{
            "clientId": int(id_),
            "clientName": options["proxy_client"]
        }

    def _prepare_add_vmpolicy_json_default(self, vm_policy_options):
        """Sets values for creating the add policy json

            Args:
                vm_policy_options    (dict)  --  main dict containing vm policy options

            Returns:
                vm_policy_json    (dict)  --  json to be passed for add policy POST request
        """
        #  setting the json values using functions for elements having nested values
        _datacenter = self._get_data_center_json(vm_policy_options)
        _entity = VirtualMachinePolicies._entity_json(vm_policy_options)
        _esxservers = [{"esxServerName": esx_server} for esx_server in vm_policy_options.get("esxServers", "")]
        _datastores = [{"dataStoreName": datastore} for datastore in vm_policy_options.get("dataStores", "")]
        _security_associations = VirtualMachinePolicies._security_associations_json(
            vm_policy_options)
        _network_names = VirtualMachinePolicies._network_names_json(vm_policy_options)

        _vm_policy_json = {
            'action': 0,        # 0 for add
            'policy': {
                "vmNameEditType": vm_policy_options.get("vm_name_edit", 1),
                "vmNameEditString": vm_policy_options.get("vm_name_edit_string", "Replicated_"),
                "createIsolatedNetwork": False,
                "isResourceGroupPolicy": True,
                "resourcePoolPath": "//",
                "destinationHyperV": {
                    "clientId": int(self._commcell_object.clients[vm_policy_options['clientName']]["id"]),
                    "clientName": vm_policy_options['clientName']
                },
                'allDataStoresSelected': vm_policy_options.get('allDataStoresSelected', False),
                'daysRetainUntil': vm_policy_options.get('daysRetainUntil', -1),
                'migrateVMs': vm_policy_options.get('migrateVMs', False),
                'senderEmailId': vm_policy_options.get('senderEmailId', ''),
                'notifyToEmailIds': vm_policy_options.get('notifyToEmailIds', ''),
                'quotaType': vm_policy_options.get('quotaType', 0),
                'maxVMQuota': vm_policy_options.get('maxVMQuota', 10),
                'namingPattern': vm_policy_options.get('namingPattern', ''),
                'description': vm_policy_options.get('description', ''),
                'enabled': vm_policy_options.get('enabled', True),
                'allowRenewals': vm_policy_options.get('allowRenewals', True),
                'disableSuccessEmail': vm_policy_options.get('disableSuccessEmail', False),
                'performAutoMigration': vm_policy_options.get('performAutoMigration', False),
                'allESXServersSelected': vm_policy_options.get('allESXServersSelected', False),
                'dataCenter': _datacenter,
                'entity': _entity,
                "proxyClientEntity": self._get_proxy_client_json(vm_policy_options),
                "networkList": [
                    {
                        "destinationNetwork": vm_policy_options.get("destination_network"),
                        "sourceNetwork": "Any Network"
                    }
                ]
            }
        }

        # adding the optional values for the json if they exist
        if _esxservers and not _vm_policy_json['policy']['allESXServersSelected']:
            _vm_policy_json['policy']['esxServers'] = _esxservers

        if _datastores and not _vm_policy_json['policy']['allDataStoresSelected']:
            _vm_policy_json['policy']['dataStores'] = _datastores

        if _network_names:
            _vm_policy_json['policy']['networkNames'] = _network_names

        if _security_associations:
            _vm_policy_json['policy']['securityAssociations'] = _security_associations

        # setting json values that are specific to a particular policy type

        if vm_policy_options["policyType"] == 4:  # for Live Mount policy
            self._prepare_add_vmpolicy_json_livemount(vm_policy_options, _vm_policy_json)
        # TODO: future support for Clone from Template policy
        elif vm_policy_options["policyType"] == 0:
            pass
        # TODO: future support for Restore from Backup policy
        else:
            pass

        return _vm_policy_json

    def _get_data_center_json(self, vm_policy_options):
        """Returns value for the datacenter json value in the add policy json

            Args:
                vm_policy_options    (dict)  --  main dict containing vm policy options

            Returns:
                _datacenter (dict)        --  datacenter json to add to vm policy json
        """
        client = self._commcell_object.clients.get(vm_policy_options['clientName'])
        vm_policy_options['clientId'] = client.client_id
        agent = client.agents.get('Virtual Server')
        instance_keys = next(iter(agent.instances._instances))
        instance = agent.instances.get(instance_keys)
        vm_policy_options['instanceId'] = instance.instance_id

        # self._set_data_center(vm_policy_options)
        _datacenter = {
            'vCenterName': vm_policy_options['vCenterName'],
            'instanceEntity': {
                'clientId': int(vm_policy_options['clientId']),
                'instanceName': vm_policy_options['clientName'],
                'instanceId': int(vm_policy_options['instanceId'])
            },
        }

        return _datacenter

    def _set_data_center(self, vm_policy_options):
        """Sets the datacenter name if provided by user, or sets the alphabetically lowest one in
            the vcenter as default

            Args:
                vm_policy_options    (dict)  --  main dict containing vm policy options

            Raises:
                SDKException:
                    if specified datacenter is not found for the corresponding virtualization
                     client

                    if no datacenter is found for the virtaulization client

                    if no response is found

                    if response is not a success
        """
        get_datacenter_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
            '<Ida_GetDataCenterListReq><policyType policyType="4" '
            'vmAllocPolicyName="" vCenterName="' + vm_policy_options['vCenterName'] +
            '"/></Ida_GetDataCenterListReq>'
        )
        response_json = self._commcell_object._qoperation_execute(request_xml=get_datacenter_xml)

        if 'dataCenterList' in response_json:
            all_nodes = response_json['dataCenterList']
            datacenter_dict = {}
            for node in all_nodes:
                if node['vCenterName'] == vm_policy_options['vCenterName']:
                    datacenter_dict[node['dataCenterName']] = node['dataCenterId']
            if 'dataCenterName' in vm_policy_options:
                if vm_policy_options['dataCenterName'] in datacenter_dict:
                    vm_policy_options['dataCenterId'] = datacenter_dict[
                        vm_policy_options['dataCenterName']]
                else:
                    # if no datacenter is found for the vclient, throw error
                    err_msg = (
                        'No datacenter found with name: {0} in virtual client: {1}'.format(
                            vm_policy_options['dataCenterName'],
                            vm_policy_options['clientName'])
                    )
                    raise SDKException('Virtual Machine', '102', err_msg)
            else:
                vm_policy_options['dataCenterName'] = next(iter(datacenter_dict))
                vm_policy_options['dataCenterId'] = datacenter_dict[vm_policy_options[
                    'dataCenterName']]
        else:
            # if no datacenter is found for the vclient, throw error
            err_msg = ('No datacenter found for virtual client: {0}'.format(
                vm_policy_options['clientName']))
            raise SDKException('Virtual Machine', '102', err_msg)

    def _clone_vm_policy(self, vm_policy_json):
        """Private method to clone a vm policy from VirtualMachinePolicy object

            Args:
                vm_policy_json    --  dict containing information to clone a particular policy
                                          along with optional information passed by user
            Returns:
                object            --  VirtualMachinePolicy object of the newly cloned policy

            Raises:
                SDKException:
                    if failed to create vm policy

                    if response is empty

                    if response is not success
        """
        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='POST', url=self._ALL_VMPOLICIES_URL, payload=vm_policy_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    if response.json()['error']['errorCode'] != 0:
                        error_message = response.json()['error']['errorMessage']
                        o_str = 'Failed to create virtual machine policy\nError: "{0}"'.format(
                            error_message)

                        raise SDKException('Virtual Machine', '102', o_str)
                # return object of VirtualMachinePolicy if there is no error in response
                self.refresh()
                return VirtualMachinePolicy(
                    self._commcell_object,
                    vm_policy_json['policy']['entity']['vmAllocPolicyName'],
                    int(vm_policy_json['policy']['entity']['policyType']),
                    int(self._vm_policies[vm_policy_json['policy']['entity']
                                          ['vmAllocPolicyName']]['id'])
                )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _prepare_add_vmpolicy_json_livemount(self, vm_policy_options, _vm_policy_json):
        """Sets values for creating the add policy json that are specific for creating Live Mount
            policy.

            Args:
                vm_policy_options (dict)  --  vm policy options provided by user

                _vm_policy_json (dict)    --  vm policy json to which Live Mount policy specific
                                            information is added
        """
        _media_agent_json = self._media_agent_json(vm_policy_options)

        _vm_policy_json['policy']['minutesRetainUntil'] = vm_policy_options.get(
            'minutesRetainUntil', 1)

        _vm_policy_json['policy']['mediaAgent'] = _media_agent_json

    @staticmethod
    def _security_associations_json(vm_policy_options):
        """Returns json for the security associations in the add policy json

            Args:
                vm_policy_options (dict)  --  vm policy options provided by user
        """
        _users = []
        if 'users' in vm_policy_options:
            # TODO: get user info using REST API. For every user, add user dict to _users
            pass
        else:
            # default - admin
            default_user = {
                "_type_": 13,
                "userGUID": "admin",
                "userName": "admin",
                "userId": 1
            }
            _users.append(default_user)

        _usergroups = []
        if 'userGroups' in vm_policy_options:
            # TODO: get usergroups info using REST API. For every userGroup, add corresponding dict
            pass

        _security_associations = {}
        if _users:
            _security_associations['users'] = _users
        if _usergroups:
            _security_associations['userGroups'] = _usergroups

        return _security_associations

    @staticmethod
    def _network_names_json(vm_policy_options):
        """Returns list of network names for the add policy json

            Args:
                vm_policy_options (dict)    --  vm policy options provided by user

            Returns:
                _network_names   (list)     --  list of network names (str)
        """
        _network_names = []
        if 'networkNames' in vm_policy_options:
            for network in vm_policy_options['networkNames']:
                _network_names.append(network)

        return _network_names

    def _media_agent_json(self, vm_policy_options):
        """Returns json for the media agent json value in the add policy json (only for LM)

            Args:
                vm_policy_options (dict)  --  vm policy options provided by user (optional)

            Returns:
                _media_agent_json (dict)  --  json containing media agent information if media
                                                agent info is passed by user
        """
        _media_agent_json = {}
        if 'mediaAgent' in vm_policy_options:
            # TODO: there can be only one MA -- validate this (whole vm_policy_options)
            media_agent = vm_policy_options['mediaAgent']
            if not self._commcell_object.media_agents.has_media_agent(media_agent):
                raise SDKException(
                    'Virtual Machine', '102',
                    'No media agent exists "{0}" exists in commserv "{1}"'.format(
                        media_agent, self._commcell_object.commserv_name))
            else:
                _media_agent_json['clientName'] = media_agent
        else:   # adding a default media agent for automation
            media_agent_dict = self._commcell_object.media_agents._media_agents
            media_agent = [ma for ma in media_agent_dict][0]
            _media_agent_json['clientName'] = media_agent

        return _media_agent_json

    @staticmethod
    def _entity_json(vm_policy_options):
        """Returns json for the entity  attribute in the add policy json

            Args:
                vm_policy_options  (dict)    --  vm policy options provided by user

            Returns:
                _entity            (dict)    --  json for the entity attribute in add policy json
        """
        _entity = {
            'vmAllocPolicyName': vm_policy_options['vmAllocPolicyName'],
            '_type_': 93,           # hardcoded
            'policyType': vm_policy_options["policyType"],
            'region': {},
        }

        return _entity

    def has_policy(self, vm_policy_name):
        """Checks if a Virtual Machine policy exists with the given name

            Args:
                policy_name (str)  --  name of the vm policy

            Returns:
                bool - boolean output whether the vm policy exists in the commcell or not

            Raises:
                SDKException:
                    if type of the vm policy name argument is not string
        """
        if not isinstance(vm_policy_name, basestring):
            raise SDKException('Virtual Machine', '101')

        return (self._vm_policies and
                vm_policy_name.lower() in self._vm_policies)

    def get(self, vm_policy_name):
        """Returns a VirtualMachinePolicy object of the specified virtual machine policy name.

            Args:
                vm_policy_name     (str)   --  name of the virtual machine policy

            Returns:
                object - instance of the VirtualMachinePolicy class for the given policy name

            Raises:
                SDKException:
                    if type of the virtual machine policy name argument is not string
                    if no virtual machine policy exists with the given name
        """
        if not isinstance(vm_policy_name, basestring):
            raise SDKException('Virtual Machine', '101')

        vm_policy_name = vm_policy_name.lower()
        if self.has_policy(vm_policy_name):
            vm_policy_type_id = int(self._vm_policies[vm_policy_name]['policyType'])
            return VirtualMachinePolicy(
                self._commcell_object,
                vm_policy_name=vm_policy_name,
                vm_policy_type_id=vm_policy_type_id,
                vm_policy_id=int(self._vm_policies[vm_policy_name]['id'])
            )
        else:
            raise SDKException(
                'Virtual Machine',
                '102',
                'No policy exists with name: {0}'.format(vm_policy_name))

    def add(
            self,
            vm_policy_name,
            vm_policy_type,
            vclient_name,
            vm_policy_options=None
    ):
        """Adds a new Virtual Machine Policy to the Commcell.

            Args:
                vm_policy_name       (str)   --  name of the new virtual machine policy to add to
                                                    the Commcell instance

                vm_policy_type       (str)   --  type of virtual machine policy to be added
                                                    ["Live Mount", "Clone From Template",
                                                    "Restore From Backup"]

                vclient_name         (str)   --  the name of the virtualization client under which
                                                    vm policy is to be added

                vm_policy_options    (dict)  --  optional dictionary passed by user to create a vm
                                                   policy. Allowed key-value pairs and input types
                                                   are given below
                    default: None

                    "allDataStoresSelected"    (Boolean)  : if all data stores are to be selected;
                                                                matters only if migrateVMs is set
                                                                to True,
                    "daysRetainUntil"          (int)      : how many days to retain backup until,
                    "migrateVMs"               (Boolean)  : migrate to datastore after expiry
                                                                (only for LiveMount),
                    "senderEmailId"            (str)      : email id of sender,
                    "minutesRetainUntil"       (int)      : how many days to retain backup until
                    "notifyToEmailIds"         (str)      : email id's to notify to; multiple
                                                                emails separated by a comma
                    "quotaType"                (int)      : number of vm's/live mounts/labs per
                                                                user,
                    "maxVMQuota"               (int)      : maximum number of VM quota,
                    "namingPattern"            (str)      : naming patter,
                    "description"              (str)      : description of vm policy,
                    "enabled"                  (Boolean)  : whether vm policy is enabled or not,
                    "allowRenewals"            (Boolean)  : whether to allow renewals or not,
                    "disableSuccessEmail"      (Boolean)  : send email on succesful creation of vm
                                                                policy,
                    "allESXServersSelected"    (Boolean)  : select all esx servers in the vcenter,
                    "dataCenterName"           (str)      : data center name for vm policy,
                    "dataStores"               list(str)  : list of data store names,
                    "esxServers"               list(str)  : list of esx server names,
                    "users"                    list(str)  : list of users (user-names) to add to vm
                                                                policy,
                    "userGroups"               list(str)  : list of usergroups (usergroup-names) to
                                                                add to vm policy,
                    "networkNames"             list(str)  : list of network names,
                    ------------------------ only for Live Mount ------------------------
                    "mediaAgent"               (str)      : media agent name for Live Mount,
                    "performAutoMigration"     (Boolean)  : automatic migration of vm

            Returns:
                object    --  object of the corresponding virtual machine policy type

            Raises:
                SDKException:
                    if type of the vm policy name argument is not string

                    if type of the vcenter name argument is not string

                    if type of virtualization client name argument is not string or None

                    if policy type is not one of the virtual machine policy types as defined

                    if the type of vm_policy_options is not dict or None

                    if vm policy already exists with the given name (case insensitive)

                    if failed to create vm policy

                    if response is empty

                    if response is not success
                """
        vm_policy_name = vm_policy_name.lower()
        vm_policy_type = vm_policy_type.lower()
        vclient_name = vclient_name.lower()
        _vm_policy_types = {'live mount': 4,
                            'clone from template': 0,
                            'restore from backup': 13}
        self.refresh()
        if (
                not isinstance(vm_policy_name, basestring)
                or not isinstance(vclient_name, basestring)
                or not isinstance(vm_policy_options, (dict, type(None)))
        ):
            raise SDKException('Virtual Machine', '101')
        elif vm_policy_type not in _vm_policy_types:
            err_msg = '{0} is not a valid virtual machine policy type.'.format(
                vm_policy_type)
            raise SDKException('Virtual Machine', '102', err_msg)
        elif self.has_policy(vm_policy_name):
            err_msg = 'Virtual Machine Policy "{0}" already exists (not case sensitive)'.format(
                vm_policy_name)
            raise SDKException('Virtual Machine', '102', err_msg)
        else:
            if not vm_policy_options:
                vm_policy_options = {}
            vm_policy_options['vmAllocPolicyName'] = vm_policy_name.lower()

            # setting the vclient name, vcenter name and policy type
            self._set_vclient_and_vcenter_names(vm_policy_options, vclient_name)
            vm_policy_options['policyType'] = _vm_policy_types[vm_policy_type]

            # preparing the json values for adding the new policy
            _vm_policy_json = self._prepare_add_vmpolicy_json_default(vm_policy_options)

            # passing the built json to create the vm policy
            (flag, response) = self._commcell_object._cvpysdk_object.make_request(
                method='POST', url=self._VMPOLICIES_URL, payload=_vm_policy_json)

            if flag:
                if response.json():
                    if 'error' in response.json():
                        if response.json()['error']['errorCode'] != 0:
                            error_message = response.json()['error']['errorMessage']
                            o_str = 'Failed to create virtual machine policy\nError: "{0}"'.format(
                                error_message)
                            raise SDKException('Virtual Machine', '102', o_str)
                    # returning object of VirtualMachinePolicy if there is no error in response
                    self.refresh()
                    return VirtualMachinePolicy(
                        self._commcell_object,
                        vm_policy_name=vm_policy_options['vmAllocPolicyName'],
                        vm_policy_type_id=int(vm_policy_options['policyType']),
                        vm_policy_id=int(self._vm_policies[vm_policy_name]['id']))
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

    def delete(self, vm_policy_name):
        """Deletes the specified virtual machine policy from the commcell.

            Args:
                vm_policy_name (str)  --  name of the virtual machine policy to delete

            Raises:
                SDKException:
                    if type of the virtual machine policy name argument is not string

                    if failed to delete virtual machine policy

                    if response is empty

                    if response is not success
        """
        if not isinstance(vm_policy_name, basestring):
            raise SDKException('Virtual Machine', '101')

        if self.has_policy(vm_policy_name):
            # retrieving the corresponding policy id for API call
            vm_policy_id = self._get_vm_policies()[vm_policy_name]['id']
            policy_delete_url = self._VMPOLICIES_URL + '/{0}'.format(vm_policy_id)

            (flag, response) = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', policy_delete_url)

            if flag:
                try:
                    if response.json():
                        if 'errorCode' in response.json() and 'errorMessage' in response.json():
                            error_message = response.json()['errorMessage']
                            output_string = 'Failed to delete virtual machine policy\nError: "{0}"'
                            raise SDKException(
                                'Virtual Machine', '102', output_string.format(error_message))
                except ValueError:
                    if response.text:
                        self.refresh()
                        return response.text.strip()
                    else:
                        raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

        else:
            raise SDKException(
                'Virtual Machine',
                '102',
                'No policy exists with name: {0}'.format(vm_policy_name))

    def refresh(self):
        """Refresh the Virtual Machine policies."""
        self._vm_policies = self._get_vm_policies()


class VirtualMachinePolicy(object):
    """Class for representing a single Virtual Machine Policy. Contains method definitions for
        common operations among all VM Policies"""

    def __new__(
            cls,
            commcell_object,
            vm_policy_name,
            vm_policy_type_id,
            vm_policy_id=None
    ):
        """Decides which instance object needs to be created"""
        if vm_policy_type_id == 4 or vm_policy_type_id == 2:  # for 'Live Mount'
            return object.__new__(LiveMountPolicy)
        # TODO: future support for 'Clone From Template'
        elif vm_policy_type_id == 6:
            return object.__new__(VirtualMachinePolicy)
        # TODO: future support for 'Restore From Backup'
        else:
            return object.__new__(VirtualMachinePolicy)

    def __init__(
            self,
            commcell_object,
            vm_policy_name,
            vm_policy_type_id,
            vm_policy_id=None
    ):
        """Initialize object of the VirtualMachinePolicy class.

            Args:
                commcell_object      (object)  --  instance of the Commcell class
                vm_policy_name       (str)     --  name of the vm policy to be created
                vm_policy_type_id    (int)     --  type of policy (integer code for vm policy)
                vm_policy_id         (int)     --  vm policy id if available (optional)

            Returns:
                object                       -- instance of the VirtualMachinePolicy class
        """
        self._commcell_object = commcell_object
        self._vm_policy_name = vm_policy_name
        self._vm_policy_type_id = vm_policy_type_id

        if vm_policy_id:
            self._vm_policy_id = str(vm_policy_id)
        else:
            self._vm_policy_id = self._get_vm_policy_id()

        self._VM_POLICY_URL = (self._commcell_object._services['GET_VM_ALLOCATION_POLICY']
                               % self._vm_policy_id)

        self._vm_policy_properties = None
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of this class."""
        return ("VirtualMachinePolicy class instance for Virtual Machine Policy: '{0}' for "
                "Commcell: '{1}'".format(self.vm_policy_name, self._commcell_object.commserv_name))

    def _get_vm_policy_id(self):
        """Gets the virtual machine policy id associated with the svirtual machine policy"""
        vm_policies = VirtualMachinePolicies(self._commcell_object)
        return vm_policies.get(self.vm_policy_name).vm_policy_id

    def _get_vm_policy_properties(self):
        """Gets the properties of the virtual machine policy.

            Returns:
                dict    --  dictionary consisting of the properties of this vm policy

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._VM_POLICY_URL
        )

        if flag:
            if response.json()['policy'][0]:        # API returns an array with one element
                return response.json()['policy'][0]
            else:
                raise SDKException('Response', 102)
        else:
            response_str = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', 101, response_str)

    def _update_vm_policy(self):
        """Updates the vm policy using a PUT request with the updated properties json.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        update_policy_json = {
            'action': 1,        # action 1 for PUT
            'policy': self._vm_policy_properties
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._VM_POLICY_URL, update_policy_json
        )

        self.refresh()

        if flag:
            if response.json():
                if 'error' in response.json():
                    if response.json()['error']['errorCode'] != 0:
                        error_message = response.json()['error']['errorMessage']
                        o_str = 'Failed to update virtual machine policy\nError: "{0}"'.format(
                            error_message)
                        raise SDKException('Virtual Machine', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_str = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_str)

    @property
    def vm_policy_name(self):
        """Treats the virtual machine policy name as a read-only attribute."""
        return self._vm_policy_name

    @property
    def vm_policy_id(self):
        """Treats the virtual machine policy id as a read-only attribute."""
        return self._vm_policy_id

    @property
    def vm_policy_type_id(self):
        """Treats the virtual machine policy type id as a read-only attribute."""
        return self._vm_policy_type_id

    def disable(self):
        """Disables a virtual machine policy if it is enabled.

            Raises:
                SDKException:
                    if vm policy is already disabled
        """
        if not self._vm_policy_properties['enabled']:
            err_msg = 'Policy is already disabled'
            raise SDKException('Virtual Machine', '102', err_msg)

        self._vm_policy_properties['enabled'] = False
        self._update_vm_policy()

    def enable(self):
        """Enables a virtual machine policy if it is disabled.

                    Raises:
                        SDKException:
                            if vm policy is already enabled
                """
        if self._vm_policy_properties['enabled']:
            err_msg = 'Policy is already enabled'
            raise SDKException('Virtual Machine', '102', err_msg)

        self._vm_policy_properties['enabled'] = True
        self._update_vm_policy()

    def clone(self, desired_vm_policy_name):
        """
        copies properties of the particular VM Policy and creates a new VM Policy with the
         specified name

        Args:
            desired_vm_policy_name   (str)  --  name of the policy that is going to be created

        Returns:
            object                          --  object of the Virtual Machine Policy

        Raises:
                SDKException:
                    if type of the desired vm policy name argument is not string

                    if a vm policy already exists by the desired vm policy name
        """
        vm_policies_object = VirtualMachinePolicies(self._commcell_object)
        if not isinstance(desired_vm_policy_name, basestring):
            raise SDKException('Virtual Machine', '101')
        elif vm_policies_object.has_policy(desired_vm_policy_name):
            err_msg = 'Policy "{0}" already exists'.format(desired_vm_policy_name)
            raise SDKException('Virtual Machine', '102', err_msg)
        else:
            import copy
            desired_vm_policy_properties = copy.deepcopy(self._vm_policy_properties)
            desired_vm_policy_name = desired_vm_policy_name.lower()
            desired_vm_policy_properties['entity']['vmAllocPolicyName'] = desired_vm_policy_name
            del desired_vm_policy_properties['entity']['vmAllocPolicyId']
            desired_vm_policy_json = {
                'action': 0,
                'policy': desired_vm_policy_properties
            }

            return vm_policies_object._clone_vm_policy(desired_vm_policy_json)

    # TODO: modify(self, vm_policy_details) - Modifies the policy as per the details passed

    def properties(self):
        """Returns the virtual machine properties"""
        return self._vm_policy_properties

    def refresh(self):
        """Refresh the Virtual Machine policy properties."""
        self._vm_policy_properties = self._get_vm_policy_properties()


class LiveMountPolicy(VirtualMachinePolicy):
    """Derived class from VirtualMachinePolicy base class for representing a single Live Mount
       Policy. Contains method definitions for operations specific for Live Mount and also
       runnning Live Mount job"""

    def __init__(
            self,
            commcell_object,
            vm_policy_name,
            vm_policy_type_id,
            vm_policy_id=None
    ):
        """Initialize object of the LiveMountPolicy class.
            Args:
                commcell_object      (object)  --  instance of the Commcell class
                vm_policy_name       (str)     --  name of the Live Mount policy
                vm_policy_type_id    (int)     -- policy type id
                vm_policy_id         (int)     --  id of the Live Mount policy, if available

            Returns:
                object                       -- instance of the LiveMountPolicy class
        """
        super(LiveMountPolicy, self).__init__(commcell_object,
                                              vm_policy_name,
                                              vm_policy_type_id,
                                              vm_policy_id)
        self._LIVE_MOUNT_JOB_URL = self._commcell_object._services['CREATE_TASK']
        self._QOPERATION_URL = self._commcell_object._services['EXECUTE_QCOMMAND']
        self._live_mounted_vm_name = None

    def _prepare_live_mount_json(self, live_mount_options):
        """Sets values for creating the add policy json
            Args:
                live_mount_options (dict)  --  live mount job  options provided by user
        """
        self._set_mounted_vm_name(live_mount_options)
        self._live_mounted_vm_name = live_mount_options['vmName']

        _associations = LiveMountPolicy.__associations_json(live_mount_options)
        _task = LiveMountPolicy._task_json()
        _subtask = LiveMountPolicy._subtask_json()
        _one_touch_response = LiveMountPolicy._one_touch_response_json(live_mount_options)
        _vm_entity = LiveMountPolicy._vm_entity_json(live_mount_options)
        _vm_info = LiveMountPolicy._vm_info_json(live_mount_options)

        # TODO: only if live mount is scheduled (non default)

        # TODO: _pattern = live_mount_json['taskInfo']['subTasks'][0]['pattern']

        # TODO:  backupOpts = live_mount_json['taskInfo']['subTasks'][0]['options']['backupOpts']
        live_mount_json = {
            'taskInfo': {
                'associations': _associations,
                'task': _task,
                'subTasks': [
                    {
                        'subTaskOperation': 1,
                        'subTask': _subtask,
                        'options': {
                            'adminOpts': {
                                'vmProvisioningOption': {
                                    'operationType': 23,
                                    'virtualMachineOption': [
                                        {
                                            'powerOnVM': True,
                                            'flags': 0,
                                            'useLinkedClone': False,
                                            'vendor': 1,
                                            'doLinkedCloneFromLocalTemplateCopy': False,
                                            'vmAllocPolicy': {
                                                'vmAllocPolicyName': self._vm_policy_name
                                            },
                                            'oneTouchResponse': _one_touch_response,
                                            'vmEntity': _vm_entity,
                                            'vmInfo': _vm_info
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }
        return live_mount_json

    def _set_mounted_vm_name(self, live_mount_options):
        """
        Sets the vm name for the live mounted vm

        Args:
                live_mount_options    (dict)  --  live mount job options

        Raises:
            SDK Exception:
                if user passes a vm name that already exists as a hidden client on the Commcell
        """
        clients = self._commcell_object.clients
        if 'vmName' in live_mount_options:
            if live_mount_options['vmName'].lower() in clients._hidden_clients:
                err_msg = 'A client already exists by the name "{0}"'.format(
                    live_mount_options['vmName'])
                raise SDKException('Virtual Machine', '102', err_msg)
        else:
            vm_name = live_mount_options['clientName'] + 'VM'
            digit = 1
            while vm_name.lower() in clients._hidden_clients:
                vm_name += str(digit)
            live_mount_options['vmName'] = vm_name

    @staticmethod
    def __associations_json(live_mount_options):
        """
        Sets the associations value for the live mount job json

            Args:
                live_mount_options    (dict)  --  live mount job options

            Returns:
                _associations          (list)  --  list containing the associations value
        """
        _associations = []
        _associations_element = {
            # 'type': 0,
            'clientName': live_mount_options['clientName'],
            # 'clientSidePackage': True,
            'subclientName': '',
            'backupsetName': '',
            'instanceName': '',
            'appName': '',
            # 'consumeLicense': True
        }
        _associations.append(_associations_element)
        return _associations

    @staticmethod
    def _task_json():
        """Sets the task value for the live mount job json

            Returns:
                _task                 (dict)  --  dict containing the task value
        """
        _task = {
            'taskType': 1,
            'initiatedFrom': 2,
            'alert': {
                'alertName': ''
            },
            'taskFlags': {
                'disabled': False
            }
        }

        # TODO: if 'schedule' is there in options, change 06 07 json

        return _task

    @staticmethod
    def _subtask_json():
        """Sets the subTask value for the live mount job json

            Returns:
                _subtask              (dict)  --  dict containing the subTask value
        """
        _subtask = {
            'subTaskType': 1,
            'operationType': 4038
        }

        # TODO: if 'schedule' in live_mount_options: add subTaskName to json

        return _subtask

    @staticmethod
    def _one_touch_response_json(live_mount_options):
        """Sets the oneTouchResponse value for the live mount job json

            Args:
                live_mount_options     (dict)  --  live mount job options

            Returns:
                _one_touch_response    (dict)  --  dict containing the oneTouchResponse value
        """
        _csinfo = LiveMountPolicy._csinfo_json(live_mount_options)
        _hwconfig = LiveMountPolicy._hwconfig_json(live_mount_options)
        _netconfig = LiveMountPolicy._netconfig_json()
        _one_touch_response = {
            'copyPrecedence': live_mount_options.get('copyPrecedence', 0),
            'version': '',
            'platform': 0,
            'dateCreated': '',
            'automationTest': False,
            'autoReboot': True,
            'csinfo': _csinfo,
            'hwconfig': _hwconfig,
            'netconfig': _netconfig,
            'dataBrowseTime': live_mount_options.get('pointInTime', {}),
            'maInfo': {
                'clientName': ''
            },
            'datastoreList': {}
        }

        return _one_touch_response

    @staticmethod
    def _csinfo_json(live_mount_options):
        """Sets the csinfo value for the live mount job json

            Args:
                live_mount_options     (dict)  --  live mount job options

            Returns:
                _csinfo                (dict)  --  dict containing the hwconfig value
        """
        _csinfo = {
            "firewallPort": 0,
            "cvdPort": 0,
            "evmgrPort": 0,
            "fwClientGroupName": "",
            "mediaAgentInfo": {},
            "mediaAgentIP": {},
            "ip": {},
            "commservInfo": {},
            "creds": {
                "password": "",
                "domainName": "",
                "confirmPassword": "",
                "userName": ""
            }
        }

        return _csinfo

    @staticmethod
    def _hwconfig_json(live_mount_options):
        """Sets the hwconfig value for the live mount job json

            Args:
                live_mount_options     (dict)  --  live mount job options

            Returns:
                _hwconfig              (dict)  --  dict containing the hwconfig value
        """
        _hwconfig = {
            'vmName': live_mount_options['vmName'],
            'magicno': '',
            'bootFirmware': 0,
            'version': '',
            'mem_size': 0,
            'cpu_count': 0,
            'nic_count': 0,
            'overwriteVm': False,
            'useMtptSelection': False,
            'ide_count': 0,
            'mtpt_count': 0,
            'scsi_count': 0,
            'diskType': 1,
            'optimizeStorage': False,
            'systemDisk': {
                'forceProvision': False,
                'bus': 0,
                'refcnt': 0,
                'size': 0,
                'name': '',
                'dataStoreName': '',
                'vm_disk_type': 0,
                'slot': 0,
                'diskType': 1,
                'tx_type': 0
            }
        }

        return _hwconfig

    @staticmethod
    def _netconfig_json():
        """Sets the netconfig value for the live mount job json

            Returns:
                _netconfig             (dict)  --  dict containing the netconfig value
        """
        _netconfig = {
            'wins': {
                'useDhcp': False
            },
            'firewall': {
                'certificatePath': '',
                'certificateBlob': '',
                'configBlob': ''
            },
            'dns': {
                'suffix': '',
                'useDhcp': False
            },
            'ipinfo': {
                'defaultgw': ''
            }
        }

        return _netconfig

    @staticmethod
    def _vm_entity_json(live_mount_options):
        """Sets the vmEntity value for the live mount job json
            Args:
                live_mount_options    (dict)  --  live mount job options

            Returns:
                _vm_entity            (dict)  --  dict containing the vmEntity value
        """
        _vm_entity = {
            'vmName': live_mount_options['vmName'],
            'clientName': live_mount_options['clientName'],
            '_type_': 88
        }

        return _vm_entity

    @staticmethod
    def _vm_info_json(live_mount_options):
        """Sets the vmInfo value for the live mount job json
            Args:
                live_mount_options    (dict)  --  live mount job options

            Returns:
                _vm_info              (dict)  --  dict containing the vmInfo value
        """
        _vm_info = {
            'advancedProperties': {
                'networkCards': [
                    {
                        'label': live_mount_options.get('network_name', '')
                    }
                ]
            },
            'vm': {
                'vmName': live_mount_options['vmName'],
                '_type_': 88
            }
        }

        # TODO: if 'original network' is chosen as option in livemount option, verify network json

        return _vm_info

    def _is_hidden_client(self, client_name):
        """Checks if specified client is a hidden client for the Commcell instance

            Args:
                client_name    (str)  -- name of the client

            Returns:
                bool                  -- boolean output whether the client is indeed a hidden
                                            client in the Commcell
        """
        clients = self._commcell_object.clients
        return clients.has_hidden_client(client_name)

    def _validate_live_mount(self, client_name):
        """Check if the specified vm has a backup for live mount

            Args:
                client_name    (str)  --  name of the vm
                client_id      (int)  --  client_id of the vm

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

                    if there is an error in the response json
        """
        clients = self._commcell_object.clients
        client_id = clients.get(client_name.lower()).client_id

        validate_live_mount_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Ida_ValidateLiveMountReq>'
            '<vmClient clientId="' + client_id + '" clientName="' + client_name + '" />'
            '</Ida_ValidateLiveMountReq>'
        )
        response_json = self._commcell_object._qoperation_execute(
            request_xml=validate_live_mount_xml)

        if response_json['error']:
            if response_json['error']['errorCode'] != 0:
                err_msg = 'Unable to validate client "{0}" for live mount. Error: {1}'.format(
                    client_name, response_json['error']['errorMessage'])
                raise SDKException('Virtual Machine', '102', err_msg)

    def view_active_mounts(self):
        """View active mounts for this Live Mount policy instance

            Returns:
                response.json()['virtualMachines']   (list) --  list of dictionary containing
                                                                    information about the vm's
                                                                    that are currently mounted
                                                                    using this ive mount policy

            Raises:
                SDKException:
                    if no response is found

                    if response is not a success
        """
        active_mount_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
                            '<Ida_GetVirtualMachinesReq><filter>'
                            '<allocationPolicy vmAllocPolicyId="' + str(self.vm_policy_id) + '"/>'
                            '</filter></Ida_GetVirtualMachinesReq>')

        response_json = self._commcell_object._qoperation_execute(request_xml=active_mount_xml)

        if 'virtualMachines' in response_json:
            return response_json['virtualMachines']

    def live_mount(
            self,
            client_vm_name,
            live_mount_options=None
    ):
        """Run Live Mount for this Live Mount policy instance

            Args:
                client_vm_name          (str)  --   client vm name for which live mount is to
                                                         be run
                live_mount_options:    (dict)  --  list of optional parameters  for each live
                                                        mount job.
                                                        Allowed key-value pairs and input types
                                                        are given below
                    default                       :  None
                    'vmName'              (str)   :  name of the new vm that will be mounted
                    'copyPrecedence'      (int)   :  number for the storage policy copy to use
                                                     Default value is zero (copy with highest
                                                     precedence is used)
                    'pointInTime'         (dict)  :  to select live mount from point in time,
                                                     provide a dict with following key-value pairs
                        "timeValue"             (str)  : date and time in below format
                                                         "yyyy-mm-dd hh:mm:ss".
                                                         "2018-06-18 16:09:00", for example.
                        "TimeZoneName"          (str)  : time zone value in given format
                                                        (MS Windows time zone options).
                                                         "(UTC-05:00) Eastern Time (US & Canada)"
                }


            Raises:
                SDKException:
                    if the vm name passed is not string

                    if the vm name passed does not exist

                    if a vm is not backed up

                    if the destination vm name (if provided) is not a string

                    if a vm with the destination vm name already exists (if provided)

            Returns:
                live_mount_job              (object)  -- Job object for the corresponding live
                                                            mount job
        """
        # check if client name is string
        if not isinstance(client_vm_name, basestring):
            raise SDKException('Virtual Machine', '101')
        # check if client is a valid hidden client
        elif not self._is_hidden_client(client_vm_name):
            err_msg = 'Client "{0}" not found in Commcell'.format(client_vm_name)
            raise SDKException('Virtual Machine', '102', err_msg)
        else:
            # check if vm to be live mounted is backed up
            #self._validate_live_mount(client_vm_name)
            
            # default options if nothing is passed
            if not live_mount_options:
                live_mount_options = {}

            live_mount_options['clientName'] = client_vm_name

            live_mount_json = self._prepare_live_mount_json(live_mount_options)

            # making a POST call for running the Live Mount job
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._LIVE_MOUNT_JOB_URL, live_mount_json
            )

            if flag:
                if response.json():
                    if 'error' in response.json():
                        if response.json()['error']['errorCode'] != 0:
                            error_message = response.json()['error']['errorMessage']
                            o_str = 'Failed to run Live Mount\nError: "{0}"'.format(error_message)
                            raise SDKException('Virtual Machine', '102', o_str)
                    # if no valid error in response
                    if 'jobIds' in response.json():
                        return Job(self._commcell_object, response.json()['jobIds'][0])
                    else:
                        raise SDKException('Virtual Machine', '102',
                                           'Failed to run live mount')
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

    @property
    def live_mounted_vm_name(self):
        """Treats the live mounted vm name as a read-only attribute."""
        return self._live_mounted_vm_name
