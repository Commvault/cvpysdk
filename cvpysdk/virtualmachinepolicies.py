# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing virtual machine related operations on the Commcell.

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

    has_policy(vm_policy_name)              --  checks if a Virtual Machine policy exists with the
                                                    given name in a particular instance

    get(vm_policy_name)                     --  returns a VirtualMachinePolicy object of the
                                                    specified virtual machine policy name

    add(vm_policy_name,
        vm_policy_json_path)                --  adds a new Virtual Machine policy to the
                                                    VirtualMachinePolicies instance,and returns an
                                                    object of corresponding vm_policy_type

    delete(vm_policy_name)                  --  removes the specified Virtual Machine policy from
                                                    the Commcell

    clone(source_ vm_policy_name,
          desired_ vm_policy_name)          --  copies properties of specified VM Policy and
                                                    creates a new VM Policy with the given name

    _prepare_add_vmpolicy_json_default
                    (vm_policy_options)     --  sets values for creating the add policy json
                                                    that are common across all vm policies

    _prepare_add_vmpolicy_json_livemount
                    (vm_policy_options)     --  sets values for creating the add policy json that
                                                     are specific for creating Live Mount policy

    _data_stores_json(options)              --  sets values for creating the datastore value in the
                                                     add policy json

    _esx_servers_json(options)              --  sets values for creating the esx server value in
                                                    the add policy json

    _security_associations_json(options)    --  sets values for creating the security associations
                                                    value in the add policy json

     _network_names_json(options)           --  sets values for creating the network names value in
                                                     the add policy json

    _data_center_json(options)              --  sets values for creating the datacenter json value
                                                    in the add policy json

    _set_data_center(options)               --  sets the datacenter name if provided by user, or
                                                    sets the alphabetically lowest one in the
                                                     vcenter as default

    _entity_json()                          --  sets values for creating the entity json value in
                                                    the add policy json

    _media_agent_json(options)              --  sets values for creating the media agent json
                                                    value in the add policy json
                                                    (only for Live Mount policy)


VirtualMachinePolicy:
    __init__(commcell_object,
             vm_policy_name,
             vm_policy_type,
             VMPolicy_id,
             vm_policy_details)                   --  initialize the instance of
                                                          VirtualMachinePolicy class for a specific
                                                          virtual machine policy of the Commcell

    __repr__()                                    --  returns a string representation of the
                                                          VirtualMachinePolicy instance

    _get_VMPolicy_id()                            --  gets the id of the VirtualMachinePolicy
                                                          instance

    _initialize_ VMPolicy _properties()           --  initializes the VM policy properties

    disable(vm_policy_name)                       --  disables the specified policy, if enabled

    enable(vm_policy_name)                        --  enables the specified policy, if disabled

    modify(vm_policy_name, vm_policy_details)     --  modifies the specified policy

    properties(vm_policy_name)                    --  gives a summary of the properties of the
                                                          specified policy


LiveMountPolicy:
    __init__(commcell_object,
             vm_policy_name,
             vm_policy_type,
             VMPolicy_id,
             vm_policy_details)                   --  initialize the instance of LiveMountPolicy
                                                          class for a specific virtual machine
                                                          policy of the Commcell

    __repr__()                                    --  returns a string representation of the
                                                          LiveMountPolicy instance

    _initialize_ LiveMountPolicy _properties()    --  initializes the LiveMountPolicy properties

    view_active_mounts()                          --  shows all active mounts for the specified
                                                          Live Mount Policy
"""

from __future__ import unicode_literals

from past.builtins import basestring

from .exception import SDKException


class VirtualMachinePolicies(object):
    """Class for representing all the Virtual Machine Policies associated with the Commcell."""

    def __init__(self, commcell_object):
        """
        Initialize object of the VirtualMachinePolicies class.
            Args:
                commcell_object (object)  --  instance of the Commcell class
            Returns:
                object - instance of the VirtualMachinePolicies class
        """

        self._commcell_object = commcell_object

        self._VMPOLICIES_URL = self._commcell_object._services['VM_ALLOCATION_POLICY']
        self._VCLIENTS_URL = self._commcell_object._services['GET_VIRTUAL_CLIENTS']
        self._QOPERATION_URL = self._commcell_object._services['EXECUTE_QCOMMAND']

        self._vm_policies = self._get_vm_policies()

    def __str__(self):
        """Representation string consisting of all virtual machine policies of the commcell.
            Returns:
                str - string of all the virtual machine policies associated with the commcell
        """

        representation_string = '''{:^5}\t{:^28}

'''.format('S. No.', 'Virtual Machine Policy')

        for (index, vm_policy) in enumerate(self._vm_policies):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, vm_policy)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Clients class."""

        return "VirtualMachinePolicies class instance for Commcell: '{0}'".format(
            self._commcell_object._headers['Host'])

    def _get_vm_policies(self):
        """Gets all the virtual machine policies associated to the commcell specified by the
            Commcell object.
            Returns:
                dict - consists of all storage policies of the commcell
                    {
                        "vm_policy1_name": vm_policy1_id,
                        "vm_policy2_name": vm_policy2_id
                    }
            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """

        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='GET', url=self._VMPOLICIES_URL)

        if flag:
            if response.json() and 'policy' in response.json():
                vm_policies = response.json()['policy']

                if vm_policies == []:
                    return {}

                vm_policies_dict = {}

                for vm_policy in vm_policies:
                    temp_name = vm_policy['entity']['vmAllocPolicyName'].lower()
                    temp_id = str(vm_policy['entity']['vmAllocPolicyId']).lower()
                    vm_policies_dict[temp_name] = temp_id

                return vm_policies_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_policy(self, vm_policy_name):
        """Checks if a Virtual Machine policy exists with the given name
            Args:
                policy_name (str)  --  name of the storage policy
            Returns:
                bool - boolean output whether the storage policy exists in the commcell or not
            Raises:
                SDKException:
                    if type of the storage policy name argument is not string
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

        if self.has_policy(vm_policy_name):
            return VirtualMachinePolicy(
                self._commcell_object,
                vm_policy_name=vm_policy_name,
                vm_policy_type=4,
                vm_policy_id=self._vm_policies[vm_policy_name])
        else:
            raise SDKException(
                'Virtual Machine',
                '102',
                'No policy exists with name: {0}'.format(vm_policy_name))

    def add(
            self,
            vm_policy_name,
            vm_policy_type,
            vcenter_name,
            vclient_name=None,
            vm_policy_options=None,
    ):
        """Adds a new Virtual Machine Policy to the Commcell.
            Args:
                vm_policy_name       (str)   --  name of the new virtual machine policy to add to
                                                    the Commcell instance

                vcenter_name         (str)   --  name of the vcenter where the vm policy is to be
                                                    added

                vclient_name         (str)   --  the name of the virtualization client under which
                                                    vm policy is to be added

                vm_policy_type       (str)   --  type of virtual machine policy to be added
                                                    ["Live Mount", "Clone From Template",
                                                    "Restore From Backup"]

                vm_policy_options    (dict)  --  optional dictionary passed by user to create a vm
                                                   policy. Allowed key-value pairs and input types
                                                   are given below

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
                    "dataStores"               list(str)  : list of data store names,
                    "esxServers"               list(str)  : list of esx server names,
                    "users"                    list(str)  : list of users (user-names) to add to vm
                                                                policy,
                    "userGroups"               list(str)  : list of usergroups (usergroup-names) to
                                                                add to vm policy,
                    "networkNames"             list(str)  : list of network names,
                    "dataCenterName"           (str)      : data center name for vm policy,
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

                    if the type of vm policy options is not dict or None

                    if vm policy already exists with the given name

                    if there is not at least one virtual machine policy already associated with
                        this commcell (workaround because datacenter id is not fetchable)

                    if vm policy is created but "enabled" attribute is set to false

                    if failed to create vm policy

                    if response is empty

                    if response is not success
                """

        _vm_policy_types = {'Live Mount': 4,
                            'Clone From Template': 0,
                            'Restore From Backup': 13}
        self._vm_policies = self._get_vm_policies()
        if (not isinstance(vm_policy_name, basestring)
                or not isinstance(vcenter_name, basestring)
                or not isinstance(vclient_name, (basestring, type(None)))
                or not isinstance(vm_policy_options, (dict, type(None)))
           ):
            raise SDKException('Virtual Machine', '101')
        elif vm_policy_type not in _vm_policy_types:
            err_msg = '{0} is not a valid virtual machine policy type.'.format(
                vm_policy_type)
            raise SDKException('Virtual Machine', '102', err_msg)
        elif self.has_policy(vm_policy_name):
            err_msg = 'Virtual Machine Policy "{0}" already exists.'.format(
                vm_policy_name)
            raise SDKException('Virtual Machine', '102', err_msg)
        elif not self._vm_policies:
            err_msg = ('No virtual machine policies found. Please create at least one vm policy'
                       'manually.')
            raise SDKException('Virtual Machine', '102', err_msg)
        else:
            if not vm_policy_options:
                vm_policy_options = {}
            vm_policy_options['vmAllocPolicyName'] = vm_policy_name
            vm_policy_options['vCenterName'] = vcenter_name

            # setting the vclient name and policy type
            self._set_vclient_name(vm_policy_options, vclient_name)
            vm_policy_options['policyType'] = _vm_policy_types[vm_policy_type]

            # preparing the json values for adding the new policy
            _vm_policy_json = self._prepare_add_vmpolicy_json_default(vm_policy_options)

            # passing the built json to create the vm policy
            (flag, response) = self._commcell_object._cvpysdk_object.make_request(
                method='POST', url=self._VMPOLICIES_URL, payload=_vm_policy_json)

            if flag:
                if response.json():
                    if 'error' in response.json():
                        error_message = response.json()['error']['errorMessage']
                        o_str = 'Failed to create virtual machine policy\nError: "{0}"'.format(
                            error_message)

                        raise SDKException('Virtual Machine', '102', o_str)
                    else:
                        # return object of corresponding Virtual Machine Policy here
                        self._vm_policies = self._get_vm_policies()
                        if _vm_policy_json['policy']['enabled'] is True:
                            return VirtualMachinePolicy(
                                self._commcell_object,
                                vm_policy_name=vm_policy_options['vmAllocPolicyName'],
                                vm_policy_type=vm_policy_options['policyType'],
                                vm_policy_id=self._vm_policies[vm_policy_name])
                        else:           # if policy is created but not enabled
                            err_msg = ('Unable to return object. VM Policy "{0}" is '
                                       'disabled.'.format(vm_policy_options['vmAllocPolicyName']))
                            raise SDKException('Virtual Machine', '102', err_msg)
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

            vm_policy_id = self._get_vm_policies()[vm_policy_name]
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
                        self._vm_policies = self._get_vm_policies()
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

    def clone(self, source_vm_policy_name, desired_vm_policy_name):
        """
        copies properties of specified VM Policy and creates a new VM Policy with the given name

        Args:
            source_vm_policy_name    (str)  --  VM policy name whose properties are going to be
                                                    cloned

            desired_vm_policy_name   (str)  --  name of the policy that is going to be created

        Returns:
            object                          --  object of the corresponding virtual machine policy
                                                    type
        """

        pass

    def _get_vclient_names(self):
        """
        returns a list of virtualization clients in the commcell

        Returns:
            list   (str)  --  list of virtualization client names (empty list if no virtualization
                                  client exists)

        Raises:
            SDKException:
                if response is not success
        """

        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='GET', url=self._VCLIENTS_URL)

        if flag:
            if response.json() and 'VSPseudoClientsList' in response.json():
                pseudo_clients = response.json()['VSPseudoClientsList']

                if not pseudo_clients:
                    return []

                client_names = []

                for pseudo_client in pseudo_clients:
                    client_names.append(pseudo_client['client']['clientName'])

                return client_names
            else:
                return []
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _set_vclient_name(self, options, vclient_name):
        """
        sets the virtualization client name; if a virtualization client name is passed, checks
         against the available virtualization clients, otherwise sets the first one in the list
         as the virtualization client

        Args:
          vclient_name    --  parameter if passed by user (or None)

        Raises:
            SDKException:
                if response is not success

                if no virtualization client exists on the Commcell

                if virtualization client with given name does not exist on this Commcell
        """

        vclient_names = self._get_vclient_names()

        if not vclient_names:
            err_msg = 'No virtualization clients exist on this Commcell.'
            raise SDKException('Virtual Machine', '102', err_msg)

        if vclient_name is None:  # choosing default vclient if not specified
            options["clientName"] = vclient_names[0]
        else:
            if vclient_name in vclient_names:
                options["clientName"] = vclient_name
            else:
                err_msg = 'Virtualization client "{0}" does not exist'.format(
                    vclient_name)
                raise SDKException('Virtual Machine', '102', err_msg)

    def _prepare_add_vmpolicy_json_default(self, vm_policy_options):
        """
        sets values for creating the add policy json

        Args:
            vm_policy_options (dict)  --  vm policy options provided by user (optional)
        """

        #  setting the json values using functions for elements having nested values

        _datacenter = self._data_center_json(vm_policy_options)
        _datastores = VirtualMachinePolicies._data_stores_json(vm_policy_options)
        _esxservers = VirtualMachinePolicies._esx_servers_json(vm_policy_options)
        _security_associations = VirtualMachinePolicies._security_associations_json(
            vm_policy_options)
        _network_names = VirtualMachinePolicies._network_names_json(vm_policy_options)
        _entity = VirtualMachinePolicies._entity_json(vm_policy_options)

        _vm_policy_json = {
            'action': 0,        # 0 for add
            'policy': {
                'allDataStoresSelected': vm_policy_options.get('allDataStoresSelected', True),
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
                'allESXServersSelected': vm_policy_options.get('allESXServersSelected', True),
                'dataCenter': _datacenter,
                'entity': _entity,
            }
        }

        # adding the optional values for the json if they exist

        if _datastores:
            _vm_policy_json['dataStores'] = _datastores

        if _esxservers:
            _vm_policy_json['esxServers'] = _esxservers

        if _network_names:
            _vm_policy_json['networkNames'] = _network_names

        if _security_associations:
            _vm_policy_json['securityAssociations'] = _security_associations

        # setting json values that are specific to a particular policy type

        if vm_policy_options["policyType"] == 4:  # for Live Mount policy
            VirtualMachinePolicies._prepare_add_vmpolicy_json_livemount(vm_policy_options,
                                                                        _vm_policy_json)
        elif vm_policy_options["policyType"] == 0:
            # for Clone from Template policy
            pass
        else:
            # for Restore from Backup policy
            pass

        return _vm_policy_json

    def _data_center_json(self, vm_policy_options):
        """
        returns value for the datacenter json value in the add policy json

        Args:
            vm_policy_options (dict)  --  vm policy options provided by user

        Returns:
            _datacenter (dict)        --  datacenter json to add to vm policy json

        """

        client = self._commcell_object.clients.get(vm_policy_options["clientName"])
        _client_id = client.client_id
        agent = client.agents.get('Virtual Server')
        instance_keys = next(iter(agent.instances._instances))
        instance = agent.instances.get(instance_keys)
        _instance_id = instance.instance_id
        self._set_data_center(vm_policy_options)
        _datacenter = {
            'dataCenterId': vm_policy_options['dataCenterId'],
            'dataCenterName': vm_policy_options['dataCenterName'],
            'vCenterName': vm_policy_options['vCenterName'],
            'instanceEntity': {'clientId': int(_client_id),
                               'clientName': vm_policy_options['clientName'],
                               'instanceId': int(_instance_id)},
        }

        return _datacenter

    def _set_data_center(self, vm_policy_options):
        """
        Sets the datacenter name if provided by user, or sets the alphabetically lowest one in the
         vcenter as default

        Args:
            vm_policy_options (dict)  --  vm policy options provided by user

        Raises:
            SDKException:
                if there is not at least one virtual machine policy already associated with this
                 Commcell
        """

        if not self._vm_policies:
            err_msg = ('No virtual machine policy found. Please create at least one vm policy '
                       'manually.')
            raise SDKException('Virtual Machine', '102', err_msg)

        # getting list of datacenters from first existing vm policy properties
        get_datacenter_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
            '<Ida_GetDataCenterListReq><policyType policyType="4" '
            'vmAllocPolicyName="' + list(self._vm_policies)[0] + '"/></Ida_GetDataCenterListReq>'
        )

        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='POST', url=self._QOPERATION_URL, payload=get_datacenter_xml)

        if flag:
            if response.json() and 'dataCenterList' in response.json():
                datacenter_list = response.json()['dataCenterList']
                if 'dataCenterName' in vm_policy_options:
                    for datacenter in datacenter_list:
                        if (
                                vm_policy_options['clientName'] ==
                                datacenter['instanceEntity']['clientName'] and
                                vm_policy_options['dataCenterName'] == datacenter['dataCenterName']
                        ):
                            vm_policy_options['dataCenterId'] = datacenter['dataCenterId']
                            return  # setting the datacenter name and id
                    err_msg = ('No datacenter found with name: {0} in virtual client: {1}'.format(
                        vm_policy_options['dataCenterName'], vm_policy_options['clientName']))
                    raise SDKException('Virtual Machine', '102', err_msg)
                else:
                    for datacenter in datacenter_list:
                        if (
                                vm_policy_options['clientName'] ==
                                datacenter['instanceEntity']['clientName']
                        ):
                            vm_policy_options['dataCenterName'] = datacenter['dataCenterName']
                            vm_policy_options['dataCenterId'] = datacenter['dataCenterId']
                            return  # setting the first datacenter for the given vclient
                    err_msg = ('No datacenter found for virtual client: {0}'.format(
                        vm_policy_options['clientName']))
                    raise SDKException('Virtual Machine', '102', err_msg)
            else:
                raise SDKException('Virtual Machine', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @staticmethod
    def _prepare_add_vmpolicy_json_livemount(vm_policy_options, _vm_policy_json):
        """
        sets values for creating the add policy json that are specific for creating Live Mount
          policy.

        Args:
            vm_policy_options (dict)  --  vm policy options provided by user

            _vm_policy_json (dict)    --  vm policy json to which Live Mount policy specific
                                            information is added
        """

        _media_agent_json = VirtualMachinePolicies._media_agent_json(vm_policy_options)

        _vm_policy_json['policy']['minutesRetainUntil'] = vm_policy_options.get(
            'minutesRetainUntil', 1)

        if _media_agent_json:
            _vm_policy_json['mediaAgent'] = _media_agent_json

    @staticmethod
    def _data_stores_json(vm_policy_options):
        """
        returns list of datastores to which live mount is to be migrated

        Args:
            vm_policy_options (dict)    --  vm policy options provided by user

        Returns:
            _datastores  (list)         --  list that stores values for datastore in add policy
                                                json
        """

        _datastores = []
        if 'dataStores' in vm_policy_options:
            vm_policy_options['migrateVms'] = True
            vm_policy_options['allDataStoresSelected'] = False
            for datastore in vm_policy_options['dataStores']:
                # insert datastore to _datastores; get type by api call

                datastore_dict = {'_type_': 92,
                                  'dataStoreName': datastore}   # datastore id needed
                _datastores.append(datastore_dict)
        elif 'migrateVMs' in vm_policy_options:
            if vm_policy_options['migrateVMs'] is True:
                # if no datastores are provided and migrateVMs is True
                # select all datastores
                vm_policy_options['allDataStoresSelected'] = True

        return _datastores

    @staticmethod
    def _esx_servers_json(vm_policy_options):
        """
        returns list of esx servers in the add policy json

        Args:
            vm_policy_options (dict)  --  vm policy options provided by user
        """

        _esxservers = []
        if 'esxServers' in vm_policy_options:
            vm_policy_options['allESXServersSelected'] = False
            for esxserver in vm_policy_options['esxServers']:
                # add each esxServe to self._esxservers;
                esxserver_dict = {'_type_': 91,
                                  'esxServerName': esxserver}  # esxserver id needed
                _esxservers.append(esxserver_dict)

        return _esxservers

    @staticmethod
    def _security_associations_json(vm_policy_options):
        """
        returns json for the security associations in the add policy json

        Args:
            vm_policy_options (dict)  --  vm policy options provided by user
        """

        _users = []
        if 'users' in vm_policy_options:
            # for user in vm_policy_options['users']:
                # add each user {}; need api for type, id
            pass
        else:
            # default - empty
            pass

        _usergroups = []
        if 'userGroups' in vm_policy_options:
            # for usergroup in vm_policy_options['userGroups']:
                # add each usergroup {}; need api for type, id
            pass
        else:
            # default empty
            pass

        _security_associations = {}
        if _users:
            _security_associations['users'] = _users
        if _usergroups:
            _security_associations['userGroups'] = _usergroups

        return _security_associations

    @staticmethod
    def _network_names_json(vm_policy_options):
        """
        returns list of network names for the add policy json

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

    @staticmethod
    def _media_agent_json(vm_policy_options):
        """
        returns json for the media agent json value in the add policy json (only for LM)

        Args:
            vm_policy_options (dict)  --  vm policy options provided by user (optional)

        Returns:
            _media_agent_json (dict)  --  json containing media agent information if media agent
                                            info is passed by user
        """

        _media_agent_json = {}
        if 'mediaAgent' in vm_policy_options:
            # there can be only one MA -- validate this
            _media_agent_json['clientName'] = vm_policy_options['mediaAgent']

        return _media_agent_json

    @staticmethod
    def _entity_json(vm_policy_options):
        """
        returns json for the entity  attribute in the add policy json

        Args:
            vm_policy_options  (dict)    --  vm policy options provided by user

        Returns:
            _entity            (dict)    --  json for the entity attribute in add policy json
        """

        _entity = {  # hardcoded
            'dataCenterId': vm_policy_options['dataCenterId'],
            'dataCenterName': vm_policy_options['dataCenterName'],
            'vmAllocPolicyName': vm_policy_options['vmAllocPolicyName'],
            '_type_': 93,           # hardcoded
            'policyType': vm_policy_options["policyType"],
            'region': {},
        }

        return _entity


class VirtualMachinePolicy(object):
    """Class for representing a single Virtual Machine Policy. Contains method definitions for
        common operations among all VM Policies"""

    def __init__(
            self,
            commcell_object,
            vm_policy_name,
            vm_policy_type,
            vm_policy_id=None,
            vm_policy_details=None,
    ):
        """
        Initialize object of the VirtualMachinePolicy class.
            Args:
                commcell_object    (object)  --  instance of the Commcell class
                vm_policy_name     (str)     --
                vm_policy_type     (int)     --
                vm_policy_id       (int)     --
                vm_policy_details  (dict)    --
            Returns:
                object - instance of the VirtualMachinePolicies class
        """

        self._vm_policy_name = vm_policy_name
        self._commcell_object = commcell_object

        if vm_policy_id:
            self._vm_policy_id = str(vm_policy_id)
        else:
            self._vm_policy_id = self._get_vm_policy_id()

        self._VM_POLICY_URL = (self._commcell_object._services['GET_VM_ALLOCATION_POLICY']
                               % self._vm_policy_id)

    def __repr__(self):
        """Representation string for the instance of this class."""

        return ("VirtualMachinePolicy class instance for Virtual Machine Policy: '{0}' for "
                "Commcell: '{1}'".format(
                    self.vm_policy_name, self._commcell_object._headers['Host']
                    )
               )

    def _get_vm_policy_id(self):
        """Gets the virtual machine policy id associated with the virtual machine policy"""

        vm_policies = VirtualMachinePolicies(self._commcell_object)
        return vm_policies._get_vm_policies()[self.vm_policy_name]

        # check this?
        # return vm_policies.get(self.vm_policy_name).vm_policy_id

    @property
    def vm_policy_name(self):
        """Treats the virtual machine policy name as a read-only attribute."""

        return self._vm_policy_name

    @property
    def vm_policy_id(self):
        """Treats the virtual machine policy id as a read-only attribute."""

        return self._vm_policy_id
