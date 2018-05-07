# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing failover specific operations.

FailoverGroups and FailoverGroup are 2 classes defined in this file.

FailoverGroups:     Class for representing all the failover groups associated
                    with a specific client

FailoverGroup:      Class for a single failover group selected for a client,
                    and to perform operations on that failover group


FailoverGroups:
    __init__(client_object)                     --  Initialise object of FailoverGroups class

    __str__()                                   --  Returns all the failover groups

    __repr__()                                  --  Returns the string for the instance of the
                                                    FailoverGroups class

    has_failover_group(
            failover_group_name)                --  Checks if failover group exists with the given name

    get(failover_group_name)                    --  Returns the FailoverGroup class object of the input
                                                    failover name

    add(failover_group_options = None)          --  Creates new failover group with failover group name

    delete(ffailover_group_name)                --  Delete failover group with failover group name

    refresh()                                   --  Refresh all failover groups created on the commcell

    #### internal methods ###
    _get_failover_groups()                      -- REST API call to get all failover groups
                                                    in the commcell

    _check_failover_group_options(              -- Checks failover group options are correct/not against
                                                    test case inputs
            failover_group_options)

    _get_failover_machines()                    -- REST API call to get all machines in the
                                                    virtualization client. It might contains
                                                    VMs/Physical machines from different sub clients but
                                                    in the same virtualization client


    _set_failover_machines(
                failover_group_options)         -- Sets failover machines in the failover group
                                                    options dict


    _prepare_clients_for_failover_group(
        failover_group_options)                 -- Prepare clients while failover group creation

    _prepare_add_failover_group_json(
                failover_group_options)         -- Constructs failover group json to create
                                                    failover group in the commcell


    _prepare_client_list_for_failover_group_json(
                            failover_group_options) -- Internal method to create client list json
                                                        to be appended to failover group json
                                                        while creating new failover group


    _prepare_vm_groups_for_failover_group_json(
                            failover_group_options) -- Internal method to create vm groups json to
                                                        be appended to failover group json
                                                        while creating new failover group

    ##### properties ######
    failover_groups()                               -- Returns all failover groups in the commcell


FailoverGroup:
    __init__(commcell_object,
            failover_group_options)                 -- Initialise object of FailoverGroup with the
                                                        specified failover name and id

    __repr__()                                      -- return the FailoverGroup name

    testboot()                                      -- Call testboot operation

    planned_failover()                              -- Call Planned failvoer operation

    unplanned_failover()                            -- Call Unplanned Failover operation

    failback()                                      -- Call failback operation

    undo_failover()                                 -- Call UndoFailover operation

    revert_failover()                               -- Call RevertFailover operation

    point_in_time_failover()                        -- Call PointInTimeFailover operation

    reverse_replication()                           -- Call ReverseReplication operation

    validate_dr_orchestration_job(jobId)            -- Validate DR orchestration job Id

    refresh()                                       -- Refresh the object properties

    ##### internal methods #####
    _get_failover_group_id()                        -- Method to get failvoer group id

    _get_failover_group_properties()                -- Get the failvoer group properties


    ##### properties #####
    failover_group_options()                        -- Returns failover group options

    failover_group_properties()                     -- Returns failover group propeerties

    failover_group_id()                             -- Returns failover group Id

    failover_group_name()                           -- Returns failover group name

    _replication_Ids()                              -- Returns replication Ids list


"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring
from ..exception import SDKException
from .drorchestrationoperations import DROrchestrationOperations


class FailoverGroups(object):
    """Class for getting all the failover groups in commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Failover groups.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the FailoverGroups class
        """
        self._commcell_object = commcell_object
        self._client_object = commcell_object.clients
        self._services = commcell_object._services

        ####### init REST API URLS #########
        self._DRGROUPS = self._commcell_object._services['DR_GROUPS']
        self._DRGROUPS_MACHINES = self._commcell_object._services['DR_GROUP_MACHINES']

        #### init variables ######
        self._vclientId = None
        self._failovergroups = None

        self.refresh()

    def __str__(self):
        """Representation string consisting of all failover groups.

            Returns:
                str - string of all the failover groups
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Failover Group Id', 'Failover Group')

        for index, failover_group in enumerate(self._failovergroups):
            sub_str = '{:^5}\t{:20}\t{:20}\n'.format(
                index + 1,
                self._failovergroups[failover_group],
                failover_group
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the FailoverGroups class."""
        return "Failover Groups for Commserv: '{0}'".format(
            self._commcell_object.commserv_name)

    def has_failover_group(self, failover_group_name):
        """Checks if failover group exists or not.

            Args:
                failover_group_name (str)  --  name of the failover group

            Returns:
                bool - boolean output whether failover group exists or not

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(failover_group_name, basestring):
            raise SDKException('FailoverGroup', '101')

        return self.failover_groups and failover_group_name.lower() in self.failover_groups

    def add(self, failover_group_options=None):
        """add new failover group exists or not.

            Args:
                failover_group_options (json) -- failover group options for creating group
                {
                    "failoverGroupName": "FailoverAutomation-vApp",
                    "failoverGroupVMs": "DRautoVM1, DRautoVM2",
                    "VirtualizationClient": "vsa-vc6.testlab.commvault.com",
                    "approvalRequired": false,
                    "initiatedFromMonitor": false
                }


            Returns:
                FailoverGroup object if successfully created else Exception is raised

            Raises:
                SDKException:
                    If Failed to construct failover group json
                    If Failed to create failover group
                    If response is empty
                    If response is not success
        """
        # check proper failover group options are set
        self._check_failover_group_options(failover_group_options)

        # construct request json
        add_failover_group_json = self._prepare_add_failover_group_json(
            failover_group_options)

        if not add_failover_group_json:
            raise SDKException(
                'FailoverGroup',
                '102',
                'Failed to construct add failover group json.')

        # passing the built json to create the vm policy
        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._DRGROUPS, add_failover_group_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create failover group \nError: "{0}"'.format(
                        error_message)

                    raise SDKException('FailoverGroup', '102', o_str)
                else:
                    # return object of corresponding Virtual Machine Policy
                    # here
                    self.refresh()
                    return self.get(failover_group_options)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, failover_group_options):
        """Returns a failover group object of the specified failover group name.

            Args:
                failover_group_options (json)  --  name of the failover group

            Returns:
                object - instance of the FailoverGroup class for the given failover group name

            Raises:
                SDKException:
                    if proper inputs are not provided
                    If Failover group doesnt exists with given name
        """
        if not isinstance(failover_group_options, dict):
            raise SDKException('FailoverGroup', '101')
        else:
            failover_group_name = failover_group_options.get(
                'failoverGroupName').lower()

            if self.has_failover_group(failover_group_name):
                return FailoverGroup(
                    self._commcell_object, failover_group_options)

            raise SDKException(
                'Failover',
                '102',
                'Failover group doesnt exists with name: {0}'.format(failover_group_name))

    def delete(self, failover_group_name):
        """ Deletes the specified failover group name.

            Args:
                failover_group_name (str)  --  name of the failover group

            Returns:


            Raises:
                SDKException:
                    if proper inputs are not provided
                    if response is empty
                    if response is not success
        """

        if not isinstance(failover_group_name, basestring):
            raise SDKException('FailoverGroup', '101')

        else:
            failover_group_name = failover_group_name.lower()

        if self.has_failover_group(failover_group_name):

            failover_group_id = self.failover_groups.get(
                failover_group_name.lower())

            if failover_group_id:
                _GET_DR_GROUP = self._commcell_object._services['GET_DR_GROUP'] % (
                    failover_group_id)

                # passing the built json to create the vm policy
                (flag, response) = self._commcell_object._cvpysdk_object.make_request(
                    method='DELETE', url=_GET_DR_GROUP)

                if flag:
                    if response.json():
                        if 'error' in response.json():
                            error_message = response.json(
                            )['error']['errorMessage']
                            o_str = 'Failed to delete failover group: {0} \nError: "{1}"'\
                                .format(failover_group_name, error_message)

                            raise SDKException('Failover', '102', o_str)
                        else:
                            # return object of corresponding Virtual Machine
                            # Policy here
                            self.refresh()

                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(
                        response.text)
                    raise SDKException('Response', '101', response_string)

        else:
            raise SDKException(
                'Failover', '102', 'No failovergroup exists with name: "{0}"'.format(
                    failover_group_name)
            )

    def refresh(self):
        """ Refresh the failover groups created in the commcell.
        Args:

        Returns:

        Raises:

        """
        self._failovergroups = self._get_failover_groups()

    @property
    def failover_groups(self):
        """ return all failover groups
        Args:

        Returns: All the failover groups in the commcell

        Raises:
        """
        if not self._failovergroups:
            self.refresh()
        return self._failovergroups

    ################# internal functions #######################
    def _check_failover_group_options(self, failover_group_options=None):
        """ checks failover group options provided from test case inputs are valid or not

            Args:
                failover_group_options (json) -- failover group options for creating group
                {
                    "failoverGroupName": "FailoverAutomation-vApp",
                    "failoverGroupVMs": "DRautoVM1, DRautoVM2",
                    "VirtualizationClient": "vsa-vc6.testlab.commvault.com",
                    "approvalRequired": false,
                    "initiatedFromMonitor": false
                }

            Returns:


            Raises:
                SDKException:
                    if proper inputs are not provided
                    if no virtualization clients exist in the commcell
                    if bo live sync schedules exist in the commcell
        """

        # failover group options json not given
        if not failover_group_options:
            failover_group_options = {}

        if 'failoverGroupName' not in failover_group_options:
            raise SDKException('FailoverGroup', '101')

        virtualization_clients = self._client_object.virtualization_clients
        if not virtualization_clients:
            err_msg = 'No virtualization clients setup on this Commcell'
            raise SDKException('FailoverGroup', '102', err_msg)

        v_client = list(virtualization_clients.keys())[0]

        failover_group_options["VirtualizationClient"] = {
            "clientName": v_client,
            "clientId": virtualization_clients.get(v_client).get("clientId"),
            "hostName": virtualization_clients.get(v_client).get("hostName")
        }

        # set internal vclient Id
        self._vclientId = self._client_object.get(v_client).client_id

        if 'machines' not in failover_group_options:
            machines = self._get_failover_machines()
            if not machines:
                err_msg = 'No live sync schedules setup on this Commcell'
                raise SDKException('FailoverGroup', '102', err_msg)

            failover_group_options["machines"] = machines

    def _get_failover_groups(self):
        """REST API call for all the failover groups in the commcell.
            Args:

            Returns:
                dict - consists of all failover groups
                    {
                         "failover_group_name1": failover_group_id1,
                         "failover_group_name2": failover_group_id2
                    }

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._DRGROUPS)

        if flag:
            if response.json() and 'vApp' in response.json():

                failover_groups_dict = {}

                for dictionary in response.json()['vApp']:
                    temp_name = dictionary['vAppEntity']['vAppName'].lower()
                    temp_id = str(dictionary['vAppEntity']['vAppId']).lower()
                    failover_groups_dict[temp_name] = temp_id

                return failover_groups_dict

        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _get_failover_machines(self):
        """ REST API call to get all machines in the virtualization client.
            It might contains VMs/Physical machines from
        different sub clients but in the same virtualization client

        Args:

        Returns: dict {
                    {
                    "client": {
                        "subclientId": 22,
                        "clientName": "testboot",
                        "instanceId": 4,
                        "clientId": 62,
                        "GUID": "5026707a-0a15-d7c6-69a9-9f781514a932"
                    },
                    "lastbackuptime": {
                        "time": 1510332496
                    },
                    "backupSet": {
                        "backupsetId": 6,
                        "backupsetName": "defaultBackupSet",
                        "applicationId": 0
                    },
                    "isVM": true,
                    "supportedOperation": 1,
                    "vendor": "VMW",
                    "copyPrecedence": 0,
                    "scheduleName": "autoSCHDL",
                    "destClient": {
                        "clientName": "testboot_SDR",
                        "GUID": "50267a1b-3939-2f52-4cba-3b941ac0840f"
                    },
                    "lastSyncTime": {
                        "time": 1510332235
                    },
                    "replicationId": 3,
                    "syncStatus": 1,
                    "failoverStatus": 0,
                    "destinationClient": {
                        "clientName": "vsa-vc6",
                        "clientId": 3
                    },
                    "destVendor": "VMW"
                },

        Raises:
            SDKException:
                if response is empty
                if response is not success

        """
        dr_group_machines = self._DRGROUPS_MACHINES % (self._vclientId)

        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='GET', url=dr_group_machines)

        if flag:
            if response.json() and 'client' in response.json():
                machines = response.json()['client']

                if not isinstance(machines, list):
                    raise SDKException('Response', '102')
                return machines

        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _prepare_add_failover_group_json(self, failover_group_options):
        """ Constructs failover group json to create failover group in the commcell

        Args: input dict of failover group options
                failover_group_options (json) -- failover group options for creating group
                {
                    "failoverGroupName": "FailoverAutomation-vApp",
                    "failoverGroupVMs": "DRautoVM1, DRautoVM2",
                    "VirtualizationClient": "vsa-vc6.testlab.commvault.com",
                    "approvalRequired": false,
                    "initiatedFromMonitor": false
                }

        Returns: dict of failover group json to be be created

        Raises:
            SDKException:
                if proper inputs are not provided
        """

        if not isinstance(failover_group_options, dict):
            raise SDKException('FailoverGroup', '101')

        if ('failoverGroupName' not in failover_group_options) or \
                ('approvalRequired' not in failover_group_options):
            raise SDKException('FailoverGroup', '101')

        failover_group_json = {
            "action": 0,
            "vApp": {
                "source": 1,
                "operationType": 16,
                "approvalRequired": failover_group_options.get("approvalRequired", False),
                "isClientGroup": False,
                "version": 2,
                "vAppEntity": {
                    "vAppName": failover_group_options.get("failoverGroupName")
                },
                "selectedEntities": [
                    {
                        "clientId": failover_group_options.get("VirtualizationClient").get("clientId"),
                        "entityId": failover_group_options.get("VirtualizationClient").get("clientId"),
                        "entityName": failover_group_options.get("VirtualizationClient").get("clientName"),
                        "instanceId": failover_group_options.get("machines")[0].get("client").get("instanceId"),
                        "_type_": 3
                    }
                ],
                "clientList": self._prepare_client_list_for_failover_group_json(failover_group_options),
                "config": self._prepare_vm_groups_for_failover_group_json(failover_group_options),

                "usersForApproval": []
            }
        }

        return failover_group_json

    def _prepare_clients_for_failover_group(self, failover_group_options):
        """ Prepare clients for constructing failover group json
        while creating new failover group

        Args: input dict of failover group options
                failover_group_options (json) -- failover group options for creating group
                {
                    "failoverGroupName": "FailoverAutomation-vApp",
                    "failoverGroupVMs": "DRautoVM1, DRautoVM2",
                    "VirtualizationClient": "vsa-vc6.testlab.commvault.com",
                    "approvalRequired": false,
                    "initiatedFromMonitor": false
                }

        Returns:

        Raises:
            SDKException:
                if proper inputs are not provided
        """
        if not isinstance(failover_group_options, dict):
            raise SDKException('FailoverGroup', '101')

        if 'machines' not in failover_group_options:
            raise SDKException('FailoverGroup', '101')

        machines = []
        if 'failoverGroupVMs' not in failover_group_options:
            # get first VM
            machines.append(failover_group_options["machines"][0])

        else:

            # iterarte over input VMs
            for vm in failover_group_options.get(
                    "failoverGroupVMs").split(","):

                vm = vm.strip()
                # iterate over all machines
                for machine in failover_group_options["machines"]:
                    if vm == machine['client']['clientName']:
                        machines.append(machine)

        return machines

    def _prepare_client_list_for_failover_group_json(
            self, failover_group_options):
        """ Create client list json to be appended to failover group json
        while creating new failover group

        Args: input dict of failover group options
                failover_group_options (json) -- failover group options for creating group
                {
                    "failoverGroupName": "FailoverAutomation-vApp",
                    "failoverGroupVMs": "DRautoVM1, DRautoVM2",
                    "VirtualizationClient": "vsa-vc6.testlab.commvault.com",
                    "approvalRequired": false,
                    "initiatedFromMonitor": false
                }

        Returns:

        Raises:
            SDKException:
                if proper inputs are not provided
        """

        if not isinstance(failover_group_options, dict):
            raise SDKException('FailoverGroup', '101')

        if 'machines' not in failover_group_options:
            raise SDKException('FailoverGroup', '101')

        clients = []

        machines = self._prepare_clients_for_failover_group(
            failover_group_options)

        # iterate over all machines
        for machine in machines:
            client = {}

            client["GUID"] = machine['client']['GUID']
            client["backupsetId"] = machine['backupSet']['backupsetId']
            client["backupsetName"] = machine['backupSet']['backupsetName']
            client["clientId"] = machine['client']['clientId']
            client["clientName"] = machine['client']['clientName']
            client["entityId"] = machine['replicationId']
            clients.append(client)

        return clients

    def _prepare_vm_groups_for_failover_group_json(
            self, failover_group_options):
        """ Create vm groups json to be appended to failover group json
        while creating new failover group

        Args: input dict of failover group options
                failover_group_options (json) -- failover group options for creating group
                {
                    "failoverGroupName": "FailoverAutomation-vApp",
                    "failoverGroupVMs": "DRautoVM1, DRautoVM2",
                    "VirtualizationClient": "vsa-vc6.testlab.commvault.com",
                    "approvalRequired": false,
                    "initiatedFromMonitor": false
                }

        Returns:

        Raises:
            SDKException:
                if proper inputs are not provided
        """

        if not isinstance(failover_group_options, dict):
            raise SDKException('FailoverGroup', '101')

        if 'machines' not in failover_group_options:
            raise SDKException('FailoverGroup', '101')

        machines = self._prepare_clients_for_failover_group(
            failover_group_options)

        vm_sequences = []

        for machine in machines:
            vm_sequence = {}
            vm_sequence["copyPrecedence"] = 0
            vm_sequence["replicationId"] = machine['replicationId']
            vm_sequence["vmInfo"] = {
                'vmGUID': machine['client']['GUID'],
                'vmName': machine['client']['clientName']}
            vm_sequence["delay"] = 1
            vm_sequence["createPublicIp"] = False
            vm_sequences.append(vm_sequence)

        # return clients

        vm_groups = {"vmGroups": [
            {
                "vmSequence": vm_sequences,
                "delay": 2,
                "groupId": 1
            }
        ]
        }
        return vm_groups


class FailoverGroup(object):
    """Class for performing failover operations on a specified failover group."""

    def __init__(self, commcell_object, failover_group_options):
        """Initialise the FailoverGroup object.

            Args:
                commcell_object (object)  --  instance of the Commcell class

                input dict of failover group options
                failover_group_options (json) -- failover group options for creating group
                {
                    "failoverGroupName": "FailoverAutomation-vApp",
                    "failoverGroupVMs": "DRautoVM1, DRautoVM2",
                    "VirtualizationClient": "vsa-vc6.testlab.commvault.com",
                    "approvalRequired": false,
                    "initiatedFromMonitor": false
                }

            Returns:
                object - instance of the FailoverGroup class
        """
        ##### local variables of these class ########
        self._commcell_object = commcell_object
        self._failover_group_options = failover_group_options
        self._services = commcell_object._services
        self._failover_group_properties = None
        self._failover_group_name = failover_group_options.get(
            "failoverGroupName")
        self._failover_group_id = self._get_failover_group_id()

        # create DROrchestrationOperations object
        self._dr_operation = DROrchestrationOperations(commcell_object)

        ##### REST API URLs #####
        self._GET_DR_GROUP = self._commcell_object._services['GET_DR_GROUP'] % (
            self._failover_group_id)

        # init local variables
        self._replicationIds = []

        self.refresh()

        # set dr orchestration options property
        self._failover_group_options['failoverGroupId'] = self._failover_group_id
        self._failover_group_options['replicationIds'] = self._replication_Ids
        self._dr_operation.dr_orchestration_options = self.failover_group_options

    @property
    def failover_group_options(self):
        """Getter failover group options"""
        return self._failover_group_options

    @property
    def failover_group_properties(self):
        """Getter failover group properties"""
        return self._failover_group_properties

    @property
    def failover_group_id(self):
        """Getter failover group Id"""
        return self._failover_group_id

    @property
    def failover_group_name(self):
        """Getter failover group name"""
        return self._failover_group_name

    @property
    def _replication_Ids(self):
        """ Returns replicationIds of the failover """

        if not self._replicationIds:
            _repIds = []

            # iterate over vm groups
            for vm_group in self.failover_group_properties.get(
                    'config').get('vmGroups'):

                # iterate over machines
                for machine in vm_group.get('vmSequence'):

                    _repIds.append(int(machine.get('replicationId', 0)))

            self._replicationIds = _repIds

        return self._replicationIds

    def refresh(self):
        """Refresh the failover group properties.
        Args:

        Returns:

        Raises:
        """
        self._get_failover_group_properties()

    def testboot(self):
        """Performs testboot failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the Testboot job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.testboot()

    def planned_failover(self):
        """Performs Planned failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the Planned Failover job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.planned_failover()

    def unplanned_failover(self):
        """Performs UnPlanned failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the Unplanned Failover job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.unplanned_failover()

    def failback(self):
        """Performs Failback operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """

        return self._dr_operation.failback()

    def undo_failover(self):
        """Performs Undo Failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.undo_failover()

    def reverse_replication(self):
        """Performs Reverse Replication operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.reverse_replication()

    def revert_failover(self):
        """Performs Revert Failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.revert_failover()

    def point_in_time_failover(self):
        """Performs Revert Failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.point_in_time_failover()

    def validate_dr_orchestration_job(self, jobId):
        """ Validates DR orchestration job of jobId
            Args:
                JobId: Job Id of the DR orchestration job

            Returns:
                bool - boolean that represents whether the DR orchestration job finished successfully or not

            Raises:
                SDKException:
                    if proper inputs are not provided
                    If failover phase failed at any stage
        """
        return self._dr_operation.validate_dr_orchestration_job(jobId)

#################### private functions #####################

    def _get_failover_group_id(self):
        """ Gets failover group Id
            Args:

            Returns: Gets the failover group id

            Raises:
        """
        failvr_groups = FailoverGroups(self._commcell_object)

        if isinstance(failvr_groups, FailoverGroups):
            failover_group_id = failvr_groups.failover_groups.get(
                str(self._failover_group_name).lower(), 0)

            if failover_group_id:
                return failover_group_id

        raise SDKException('FailoverGroup', '101')

    def _get_failover_group_properties(self):
        """ Gets failover group properties
            Args:

            Returns: Gets the failover group properties dict

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._GET_DR_GROUP)

        if flag:
            if response.json() and 'vApp' in response.json():
                self._failover_group_properties = response.json()['vApp'][0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)
