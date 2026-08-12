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

"""Main file for getting Recovery job details and phases

RecoveryJob: Class for representing all the Recovery jobs

RecoveryJob(Job):
    __init__(commcell_object,
            job_id)                 -- Initialise object of RecoveryJob
    _get_recovery_job_stats()       -- Gets the Recovery job statistics
    get_phases()                    -- Gets the phases of the Recovery job
    get_restore_vm_from_recovery_job()  -- Waits for RESTORE_VM phase and returns its job ID
    wait_for_restore_phase_completion() -- Waits for all RESTORE_VM phases to complete
"""

import time
from typing import TYPE_CHECKING
from cvpysdk.job import Job
from cvpysdk.exception import SDKException
from cvpysdk.drorchestration.dr_orchestration_job_phase import DRJobPhases, DRJobPhaseToText

if TYPE_CHECKING:
    from cvpysdk.commcell import Commcell


class RecoveryJob(Job):
    """
    Class for managing and performing Recovery Job operations within a CommCell environment.

    This class provides an interface for interacting with recovery jobs, including
    initialization, retrieval of job statistics, and management of job properties.
    It also offers methods to access recovery job phases and restore virtual machines
    from recovery jobs with configurable retry and frequency options.

    Key Features:
        - Initialization of recovery job instances with CommCell context and job ID
        - Retrieval of recovery job statistics
        - Initialization and management of job properties
        - Access to recovery job phases
        - Restoration of virtual machines from recovery jobs with retry and frequency controls
        - String representation for easy identification

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', job_id: int) -> None:
        """Initialize a RecoveryJob instance with the specified Commcell connection and job ID.

        Args:
            commcell_object: The Commcell object representing the active Commcell session.
            job_id: The unique identifier for the recovery job.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> recovery_job = RecoveryJob(commcell, 12345)
            >>> print("Recovery job initialized with ID:", recovery_job.job_id)
        #ai-gen-doc
        """
        self._recovery_job_stats = None

        service_url = commcell_object._services['DRORCHESTRATION_JOB_STATS']
        self._RECOVERY_STATS = service_url % job_id

        Job.__init__(self, commcell_object, job_id)

    def __repr__(self) -> str:
        """Return a string representation of the RecoveryJob object.

        This method provides a developer-friendly string that can be used to 
        inspect the RecoveryJob instance, typically for debugging purposes.

        Example:
            >>> job = RecoveryJob()
            >>> print(repr(job))
            >>> # Output will display the RecoveryJob object's details

        #ai-gen-doc
        """
        representation_string = 'RecoveryJob class instance for job id: "{0}"'
        return representation_string.format(self.job_id)

    def _get_recovery_job_stats(self) -> list:
        """Retrieve statistics for the current Recovery Job.

        This method returns a list of dictionaries containing detailed statistics 
        about the recovery job, including job IDs, recovery entity IDs, replication IDs, 
        phase information, client details, and vApp details.

        Returns:
            list: A list of dictionaries, each representing the statistics for a recovery job. 
            Each dictionary contains keys such as 'jobId', 'recoveryEntityId', 'replicationId', 
            'phase', 'client', and 'vapp', with nested structures for detailed phase and job info.

        Example:
            >>> stats = recovery_job._get_recovery_job_stats()
            >>> for job_stat in stats:
            ...     print(f"Job ID: {job_stat['jobId']}, Client: {job_stat['client']['clientName']}")
            >>> # Access phase details
            >>> if stats and 'phase' in stats[0]:
            ...     for phase in stats[0]['phase']:
            ...         print(f"Phase: {phase['phase']}, Status: {phase['status']}")
        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._RECOVERY_STATS)

        if flag:
            if response.json() and 'job' in response.json():
                return response.json()['job'] or []
            elif response.json() and 'errors' in response.json():
                errors = response.json().get('errors', [{}])
                error_list = errors[0].get('errList', [{}])
                error_code = error_list[0].get('errorCode', 0)
                error_message = error_list.get('errLogMessage', '').strip()
                if error_code != 0:
                    response_string = self._commcell_object._update_response_(
                        error_message)
                    raise SDKException('Response', '101', response_string)
            else:
                if response.json():
                    raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_job_properties(self) -> None:
        """Initialize the job properties and set up the Recovery job details.

        This method prepares all necessary job properties and initializes the details
        required for a Recovery job. It should be called before performing any recovery
        operations to ensure the job is properly configured.

        Example:
            >>> recovery_job = RecoveryJob()
            >>> recovery_job._initialize_job_properties()
            >>> # The RecoveryJob instance is now initialized and ready for use

        #ai-gen-doc
        """
        Job._initialize_job_properties(self)
        self._recovery_job_stats = self._get_recovery_job_stats()

    def get_phases(self) -> dict:
        """Retrieve the phases of the recovery job for each source and destination VM pair.

        Returns:
            dict: A dictionary where each key is a source VM name, and the value is a list of dictionaries,
            each representing a phase of the recovery job. Each phase dictionary contains:
                - 'phase_name': Enum representing the phase short name and full name mapping.
                - 'phase_status': int (0 for success, 1 for failed).
                - 'start_time': int, timestamp of the start of the phase.
                - 'end_time': int, timestamp of the end of the phase.
                - 'machine_name': str, the name of the machine executing the job.
                - 'error_message': str, error message if any.

        Example:
            >>> phases = recovery_job.get_phases()
            >>> for vm, phase_list in phases.items():
            ...     print(f"VM: {vm}")
            ...     for phase in phase_list:
            ...         print(f"  Phase: {phase['phase_name']}, Status: {phase['phase_status']}")
            ...         if phase['error_message']:
            ...             print(f"    Error: {phase['error_message']}")

        #ai-gen-doc
        """
        job_stats = {}
        if not self._recovery_job_stats:
            return job_stats
        for pair_stats in self._recovery_job_stats:
            phases = []
            for phase in pair_stats.get('phase', []):
                phases.append({
                    # We use common enum for job phases
                    'phase_name': DRJobPhaseToText[DRJobPhases(phase.get('phase', '')).name]
                    if phase.get('phase', '') else '',
                    'phase_status': phase.get('status', 1),
                    'start_time': phase.get('startTime', {}).get('time', ''),
                    'end_time': phase.get('endTime', {}).get('time', ''),
                    'machine_name': phase.get('entity', {}).get('clientName', ''),
                    'error_message': phase.get('phaseInfo', {}).get('job', [{}])[0].get('failure', {})
                                     .get('errorMessage', ''),
                    'job_id': str(phase.get('phaseInfo', {}).get('job', [{}])[0].get('jobid', '')),
                })
            job_stats[str(pair_stats.get('client', {}).get('clientName', ''))] = phases
        return job_stats

    def get_restore_vm_from_recovery_job(self, entity: str, max_retries: int = 30, check_frequency: int = 10) -> int:
        """Retrieve the restore job ID for a specific VM entity during a recovery job.

        This method attempts to locate the restore job ID associated with the given VM entity
        by polling the recovery job status. It will retry up to `max_retries` times, waiting
        `check_frequency` seconds between each attempt.

        Args:
            entity: The name of the VM entity for which to retrieve the restore job ID.
            max_retries: The maximum number of polling attempts to check for the restore phase. Default is 30.
            check_frequency: The interval in seconds between each polling attempt. Default is 10.

        Returns:
            The job ID (int) of the restore VM job if found.

        Raises:
            Exception: If the RESTORE_VM phase is not found after the specified number of retries.

        Example:
            >>> recovery_job = RecoveryJob()
            >>> restore_job_id = recovery_job.get_restore_vm_from_recovery_job('VM01')
            >>> print(f"Restore job ID for VM01: {restore_job_id}")

        #ai-gen-doc
        """
        for attempt in range(max_retries):
            self._initialize_job_properties()
            phases = self.get_phases().get(entity, [])

            for phase in phases:
                if phase.get('phase_name').name == "RESTORE_VM":
                    restore_job_id = phase.get('job_id')
                    return restore_job_id

            time.sleep(check_frequency)

        raise Exception(f"Failed to locate RESTORE_VM phase for VM '{entity}' in job {self.job_id}")

    def wait_for_restore_phase_completion(self, max_retries: int = 30, check_frequency: int = 10) -> dict:
        """Wait for RESTORE_VM jobs to complete for all entities in this recovery job.

        Polls until all VM entities appear in the job phases, then calls
        ``get_restore_vm_from_recovery_job`` for each entity and waits for every
        restore job to finish.

        Args:
            max_retries: The maximum number of polling attempts when waiting for entities. Default is 30.
            check_frequency: The interval in seconds between each polling attempt. Default is 10.

        Raises:
            Exception: If no entities appear in the job phases after all retries.

        Returns:
            dict: Mapping of entity name to completed Job object, e.g. ``{'VM1': <Job 123>}``.

        Example:
            >>> recovery_job = RecoveryJob(commcell, 2829114)
            >>> restore_jobs = recovery_job.wait_for_restore_phase_completion()

        #ai-gen-doc
        """
        entities = []
        for _ in range(max_retries):
            self._initialize_job_properties()
            all_phases = self.get_phases()
            entities = [entity for entity in all_phases.keys() if entity]  # skip job-level '' key
            if entities:
                break
            time.sleep(check_frequency)
        else:
            raise Exception(
                f"No VM entities found in job {self.job_id} after {max_retries} retries"
            )

        restore_jobs = {}
        for entity in entities:
            restore_job_id = self.get_restore_vm_from_recovery_job(entity, max_retries, check_frequency)
            restore_job = Job(self._commcell_object, int(restore_job_id))
            restore_job.wait_for_completion()
            restore_jobs[entity] = restore_job
        return restore_jobs
        
    def wait_for_create_access_node_phase(self, max_retries: int = 30, check_frequency: int = 10) -> int:
        """Wait until the Create Access Node phase (phase 83) has started and return its job ID.

        The CREATE_ACCESS_NODE phase is a job-level phase (not tied to a specific VM pair),
        so it is stored under the empty-string key in get_phases().

        Args:
            max_retries: The maximum number of polling attempts. Default is 30.
            check_frequency: The interval in seconds between each polling attempt. Default is 10.

        Returns:
            The job ID (int) of the Create Access Node job.

        Raises:
            Exception: If the CREATE_ACCESS_NODE phase is not found after the specified number of retries.

        Example:
            >>> recovery_job = RecoveryJob(commcell, 2829114)
            >>> access_node_job_id = recovery_job.wait_for_create_access_node_phase()
            >>> print(f"Create Access Node job ID: {access_node_job_id}")

        #ai-gen-doc
        """
        for attempt in range(max_retries):
            self._initialize_job_properties()
            # CREATE_ACCESS_NODE is a job-level phase with no clientName, keyed as '' in get_phases()
            phases = self.get_phases().get('', [])

            for phase in phases:
                if phase.get('phase_name') and phase.get('phase_name').name == "CREATE_ACCESS_NODE":
                    job_id = phase.get('job_id')
                    if job_id is not None:
                        return int(job_id)

            time.sleep(check_frequency)

        raise Exception(
            f"Failed to locate CREATE_ACCESS_NODE phase in job {self.job_id} after {max_retries} retries"
        )