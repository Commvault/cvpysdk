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

"""Main file for performing failover specific operations.

ReplicationMonitor: Class for representing all the dr orchestration operations
from Replication monitor


ReplicationMonitor:
    __init__(commcell_object,
            replication_monitor_options)            -- Initialise object of ReplicationMonitor

    __repr__()                                      -- Return the ReplicationMonitor name

    testboot()                                      -- Call testboot operation

    planned_failover()                              -- Call Planned failvoer operation

    unplanned_failover()                            -- Call Unplanned Failover operation

    failback()                                      -- Call failback operation

    undo_failover()                                 -- Call UndoFailover operation

    revert_failover()                               -- Call RevertFailover operation

    point_in_time_failover()                        -- Call PointInTimeFailover operation

    reverse_replication()                           -- Schedule and call ReverseReplication operation

    schedule_reverse_replication()                  -- Schedule ReverseReplication

    force_reverse_replication()                     -- Call ReverseReplication operation

    validate_dr_orchestration_job(jobId)            -- Validate DR orchestration job Id

    refresh()                                       -- Refresh the object properties

    ##### internal methods #####
    _get_replication_monitor()                      -- Gets replication monitor

    _get_snapshot_list()                            -- Gets snapshot list for the destination client

    ##### properties #####
    _replication_Ids()                              -- Returns replication Ids list

    replication_monitor_options()                   -- Returns replication monitor options


"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ..exception import SDKException
from .drorchestrationoperations import DROrchestrationOperations


class ReplicationMonitor(object):
    """Class for performing DR orchestration operations on ReplicationMonitor."""

    def __init__(self, commcell_object, replication_monitor_options):
        """Initialise the ReplicationMonitor object.

            Args:
                commcell_object (object)  --  instance of the Commcell class

                input dict of replication monitor options
                replication_monitor_options (json) -- replication monitor options
                {
                    "VirtualizationClient": "",
                    "approvalRequired": False,
                    "skipDisableNetworkAdapter": False
                    "initiatedFromMonitor": True,
                    "vmName": 'DRVM1'
                }

            Returns:
                object - instance of the ReplicationMonitor class
        """
        ##### local variables of these class ########
        self._commcell_object = commcell_object
        self._replication_monitor_options = replication_monitor_options
        self._services = commcell_object._services

        # create DROrchestrationOperations object
        self._dr_operation = DROrchestrationOperations(commcell_object)

        ##### REST API URLs #####
        self._REPLICATION_MONITOR = self._commcell_object._services['REPLICATION_MONITOR']

        # init local variables
        self._replicationId = None

        self.refresh()

        # set dr orchestration options property
        self._replication_monitor_options['replicationIds'] = self._replication_Ids
        self._dr_operation.dr_orchestration_options = self.replication_monitor_options

    def __repr__(self):
        """String representation of the instance of this class."""
        return 'ReplicationMonitor instance for Commcell'

    @property
    def _replication_Ids(self):
        """ Returns replicationIds of the failover """
        if not self._replicationId:

            vm_name = self.replication_monitor_options.get("vmName", "")
            _rep_Ids = []

            if not vm_name:

                # get the first VM if input vm doesnt exist
                vm = self.replication_monitor[0]
                _rep_Ids.append(vm.get('replicationId', 0))

            else:
                # adds support to a list of VM names
                # for backward compatibility, converts a single string to a list
                if not isinstance(vm_name, list):
                    assert isinstance(vm_name, str)
                    vm_name = [vm_name]

                # makes the entire list lower case
                vm_name = list(map(lambda x : str(x).lower(), vm_name))

                # iterate through all the vms
                for _vm in self.replication_monitor:
                    if str(_vm.get("sourceName")).lower() in vm_name:
                        _rep_Ids.append(_vm.get("replicationId", 0))

            self._replicationId = _rep_Ids

        return self._replicationId

    @property
    def replication_monitor_options(self):
        """Getter replication monitor"""
        return self._replication_monitor_options

    @property
    def replication_monitor(self):
        """Getter replication monitor"""
        return self._replication_monitor

    def refresh(self):
        """Refresh the replication monitor.
        Args:

        Returns:

        Raises:
        """
        self._get_replication_monitor()

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
        """Schedules and calls Reverse Replication

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the reverse replication job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.reverse_replication()

    def schedule_reverse_replication(self):
        """Schedules Reverse Replication.

            Args:

            Returns:
                (TaskId) - TaskId of the scheduling reverse replication job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.schedule_reverse_replication()

    def force_reverse_replication(self):
        """Performs one reverse replication operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the reverse replication job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        return self._dr_operation.force_reverse_replication()

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
        snapshot_list = self._get_snapshot_list()

        if len(snapshot_list) == 0:
            raise SDKException("ReplicationMonitor", "101",
                               "No snapshot is found.")

        # fetch the first snapshot to run
        return self._dr_operation.point_in_time_failover(
            snapshot_list[0]["timestamp"],
            self._replication_monitor_options['replicationIds'][0])

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

    def _get_replication_monitor(self):
        """ Gets replication monitor options
            Args:

            Returns: Gets the Replication monitor options dict

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._REPLICATION_MONITOR)

        if flag:
            if response.json():
                self._replication_monitor = response.json()['siteInfo']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _get_snapshot_list(self):
        """ Gets snapshot list for the destination client

            Args:

            Returns:
                list of dict: list of snapshot information
        """
        vm_name = self.replication_monitor_options.get("vmName", "")
        vm = None

        # parses vm information from the replication monitor
        if not vm_name:
            vm = self.replication_monitor[0]
        else:
            for _vm in self.replication_monitor:
                if str(_vm.get("sourceName")).lower() == str(vm_name).lower():
                    vm = _vm
                    break

        # we only need the information about destination guid
        destination_guid = vm["destinationGuid"]
        instance_id = vm["parentSubclient"]["instanceId"]

        return self._dr_operation.get_snapshot_list(destination_guid, instance_id)
