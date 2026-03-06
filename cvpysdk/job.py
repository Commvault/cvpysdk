# -*- coding: utf-8 -*-
# pylint: disable=W0104, R0205, R1710

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

"""Main file for performing operations on a job.

JobController:  Class for managing jobs on this commcell

JobManagement:  Class for performing Job Management operations

Job:            Class for keeping track of a job and perform various operations on it.


JobController
=============

    __init__(commcell_object)   --  initializes the instance of JobController class associated
    with the specified commcell

    __str__()                   --  returns the string representation of the active jobs
    on this commcell

    __repr__()                  --  returns the string representation of the object of this class,
    with the commcell it is associated with

    _get_jobs_list()            --  executes the request, and parses and returns the jobs response

    _get_jobs_request_json(**options)
                                --  Returns the request json for the jobs request

    _modify_all_jobs(operation_type=None)
                                --  executes a request on the server to suspend/resume/kill all
                                        the jobs on the commserver.

    get_active_job_summary()    --  Returns a dict with summary of active jobs

    all_jobs()                  --  returns all the jobs on this commcell

    active_jobs()               --  returns the dict of active jobs and their details

    finished_jobs()             --  retutns the dict of finished jobs and their details

    get()                       --  returns the Job class instance for the given job id

    kill_all_jobs()             -- Kills all jobs on the commcell

    resume_all_jobs()           -- Resumes all jobs on the commcell

    suspend_all_jobs()          -- Suspends all jobs on the commcell


JobManagement
==============

    __init__(commcell_object)                                       --  initialise object of the JobManagement class

    _set_jobmanagement_settings()                                   --  sets the jobmanagement settings

    _refresh()                                                      --  refresh the job management settings

     set_general_settings(settings)                                 --  sets the general settings of job management

     set_priority_settings(settings)                                --  sets the priority settings of job management

     set_restart_settings(settings)                                 --  sets the restart settings of job management

     set_update_settings(settings)                                  --  sets the update settings of job management

     job_priority_precedence                                        --  gets the job priority precedence

     job_priority_precedence(priority_type)                         --  sets the job priority precedence property

     start_phase_retry_interval                                     --  gets the start phase retry interval in
                                                                        (minutes)

     start_phase_retry_interval(minutes)                            --  sets the start phase retry interval property

     state_update_interval_for_continuous_data_replicator           --  gets the start phase retry interval in
                                                                        (minutes)

     state_update_interval_for_continuous_data_replicator(minutes)  --  sets the state update interval for continuous
                                                                        data replicator

     allow_running_jobs_to_complete_past_operation_window           --  gets the allow running jobs to complete past
                                                                        operation window(True/False)

     allow_running_jobs_to_complete_past_operation_window(flag)     --  sets the allow running jobs to complete past
                                                                        operation window

     job_alive_check_interval_in_minutes                            --  gets the job alive check interval in (minutes)

     job_alive_check_interval_in_minutes(minutes)                   --  sets the job alive check interval in minutes

     queue_scheduled_jobs                                           --  gets the queue scheduled jobs(True/False)

     queue_scheduled_jobs(flags)                                    --  sets the queue scheduled jobs

     enable_job_throttle_at_client_level                            --  gets the enable job throttle at client level
                                                                        (True/False)

     enable_job_throttle_at_client_level(flag)                      --  sets the enable job throttle at client level

     enable_multiplexing_for_db_agents                              --  gets the enable multiplexing for db agents
                                                                        (True/False)

     enable_multiplexing_for_db_agents(flag)                        --  sets the enable multiplexing for db agents

     queue_jobs_if_conflicting_jobs_active                          --  gets the queue jobs if conflicting jobs active
                                                                        (True/False)

     queue_jobs_if_conflicting_jobs_active(flag)                    --  sets the queue jobs if conflicting jobs active

     queue_jobs_if_activity_disabled                                --  gets the queue jobs if activity disabled
                                                                        (True/False)

     queue_jobs_if_activity_disabled(flag)                          --  sets the queue jobs if activity disabled

     backups_preempts_auxilary_copy                                 --  gets the backups preempts auxilary copy
                                                                        (True/False)

     backups_preempts_auxilary_copy(flag)                           --  sets the backups preempts auxilary copy

     restore_preempts_other_jobs                                    --  gets the restore preempts other jobs
                                                                        (True/False)

     restore_preempts_other_jobs(flag)                               --  sets the restore preempts other jobs

     enable_multiplexing_for_oracle                                  --  gets the enable multiplexing for oracle
                                                                        (True/False)

     enable_multiplexing_for_oracle(flag)                            --  sets the enable multiplexing for oracle

     job_stream_high_water_mark_level                                --  gets the job stream high water mark level

     job_stream_high_water_mark_level(level)                         --  sets the job stream high water mark level

     backups_preempts_other_backups                                  --  gets the backups preempts other backups
                                                                        (True/False)

     backups_preempts_other_backups(flag)                            --  sets the backups preempts other backups

     do_not_start_backups_on_disabled_client                         --  gets the do not start backups on
                                                                         disabled client(True/False)

     do_not_start_backups_on_disabled_client(flag)                   --  sets the do not start backups
                                                                         on disabled client

     get_restart_setting(jobtype)                                    --  gets the restart settings of a specific
                                                                         jobtype

     get_priority_setting(jobtype)                                   --  gets the priority setting of a specific
                                                                         jobtype

     get_update_setting(jobtype)                                     --   gets the update settings of a specific
                                                                          jobtype

     get_restart_settings                                            --  gets the restart settings of job management

     get_priority_settings                                           --  gets the priority settings of job management

     get_update_settings                                             --  gets the update settings of job management


Job
===

    __init__()                  --  initializes the instance of Job class associated with the
    specified commcell of job with id: 'job_id'

    __repr__()                  --  returns the string representation of the object of this class,
    with the job id it is associated with

    _is_valid_job()             --  checks if the job with the given id is a valid job or not

    _get_job_summary()          --  gets the summary of the job with the given job id

    _get_job_details()          --  gets the details of the job with the given job id

    _initialize_job_properties()--  initializes the properties of the job

    _wait_for_status()          --  waits for 6 minutes or till the job status is changed
    to given status, whichever is earlier

    wait_for_completion()       --  waits for the job to finish, (job.is_finished == True)

    is_finished()               --  checks for the status of the job.

                                        Returns True if finished, else False

    pause()                     --  suspend the job

    resume()                    --  resumes the job

    resubmit()                  --  to resubmit the job

    kill()                      --  kills the job

    refresh()                   --  refresh the properties of the Job

    advanced_job_details()      --  Returns advanced properties for the job

    get_events()                --  returns the commserv events for the job

    get_child_jobs()            --  Returns the child jobs


Job instance Attributes
-----------------------

**job.is_finished**                 --  specifies whether the job is finished or not    (True / False)

**job.client_name**                 --  returns the name of the client, job is running for

**job.agent_name**                  --  returns the name of the agent, job is running for

**job.instance_name**               --  returns the name of the instance, job is running for

**job.backupset_name**              --  returns the name of the backupset, job is running for

**job.subclient_name**              --  returns the name of the subclient, job is running for

**job.status**                      --  returns the current status of the job
                                        (Completed / Suspended / Waiting / ... / etc.)
        http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm
        please refer status section in above doc link for complete list of status available

**job.job_id**                      --  returns the id of the job

**job.job_type**                    --  returns the type of the job

**job.backup_level**                --  returns the backup level (if applicable), otherwise None

**job.start_time**                  --  returns the start time of the job

**job.end_time**                    --  returns the end time of the job

**job.delay_reason**                --  reason why the job was delayed

**job.pending_reason**              --  reason if job went into pending state

**job.phase**                       --  returns the current phase of the job

**job.summary**                     --  returns the dictionary consisting of the full summary of the job

**job.attempts**                    --  returns the dictionary consisting of the attempt details of the job

**job.username**                    --  returns the username with which the job started

**job.userid**                      --  returns the userid with which the job started

**job.details**                     --  returns the dictionary consisting of the full details of the job

**job.num_of_files_transferred**    -- returns the current number of files transferred for the job.

**job.state**                       -- returns the current state of the job.

**job.job_end_time**                -- returns the job end time in unix time stamp.

**job.num_of_objects**              -- returns the number of items backedup in a backup job.

ErrorRule
=========

    _get_xml_for_rule()             --  Returns the XML for a given rule's dictionary of key value pairs.

    add_error_rule()                --  Add new error rules as well as update existing rules.

    _modify_job_status_on_errors()  --  Internally used to enable or disable job status on errors.

    enable()                        --  Enable an error rule for a specific iDA using _modify_job_status_on_errors.

    disable()                       --  Disable an error rule for a specific iDA using _modify_job_status_on_errors.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import time
import copy

from .exception import SDKException
from .constants import AdvancedJobDetailType, ApplicationGroup
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
if TYPE_CHECKING:
    from cvpysdk.commcell import Commcell

class JobController(object):
    """
    Controller class for managing jobs associated with a CommCell.

    The JobController class provides a comprehensive interface for interacting with
    and controlling jobs within a CommCell environment. It enables users to retrieve
    job summaries, query job lists based on status and filters, and perform bulk
    operations on jobs such as suspending, resuming, or killing all jobs. The class
    also supports fetching details of individual jobs by job ID.

    Key Features:
        - Retrieve active job summaries
        - List all jobs, active jobs, or finished jobs with filtering options
        - Perform bulk operations: suspend, resume, or kill all jobs
        - Modify jobs based on operation type
        - Fetch details of a specific job by job ID
        - Internal utilities for job request and job list management

    Args:
        commcell_object: The CommCell object to associate with job operations.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize the JobController with a Commcell connection.

        Args:
            commcell_object: Instance of the Commcell class used to access job details.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> job_controller = JobController(commcell)
            >>> # The JobController instance can now be used to manage and retrieve job details

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

    def __str__(self) -> str:
        """Return a formatted string representation of all active jobs on this Commcell.

        The string includes a table with columns for Job ID, Operation, Status, Agent type, 
        Job type, Progress, and Pending Reason, providing a clear overview of all currently 
        active jobs managed by this JobController.

        Returns:
            str: A formatted string listing all active jobs and their details.

        Example:
            >>> job_controller = JobController(commcell_object)
            >>> print(str(job_controller))
            >>> # Output will display a table of active jobs with their status and details

        #ai-gen-doc
        """
        jobs_dict = self.active_jobs()

        representation_string = '{:^5}\t{:^25}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'Job ID', 'Operation', 'Status', 'Agent type', 'Job type', 'Progress', 'Pending Reason'
        )

        for job in jobs_dict:
            sub_str = '{:^5}\t{:25}\t{:20}\t{:20}\t{:20}\t{:20}%\t{:^20}\n'.format(
                job,
                jobs_dict[job]['operation'],
                jobs_dict[job]['status'],
                jobs_dict[job]['app_type'],
                jobs_dict[job]['job_type'],
                jobs_dict[job]['percent_complete'],
                jobs_dict[job]['pending_reason']
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return a string representation of the JobController instance.

        This method provides a human-readable description of the JobController object,
        typically used for debugging and logging purposes.

        Returns:
            A string indicating that this is a JobController class instance for Commcell.

        Example:
            >>> job_controller = JobController(commcell_object)
            >>> print(repr(job_controller))
            JobController class instance for Commcell

        #ai-gen-doc
        """
        return "JobController class instance for Commcell"

    def _get_jobs_request_json(self, **options: Any) -> Dict[str, Any]:
        """Construct the request JSON for retrieving job information.

        This method builds a request payload for querying jobs from the server, 
        allowing customization via keyword arguments. The options dictionary can 
        include filters such as job category, paging configuration, client lists, 
        job types, and entity details.

        Args:
            **options: Arbitrary keyword arguments to customize the job request.
                Available options:
                    category (str): Category of jobs to retrieve. Valid values: 'ALL', 'ACTIVE', 'FINISHED'. Default is 'ALL'.
                    limit (int): Number of jobs to return. Default is 20.
                    offset (int): Starting index for jobs to return. Default is 0.
                    lookup_time (int): Retrieve jobs older than this number of hours. Default is 5.
                    show_aged_jobs (bool): Whether to include aged jobs. Default is False.
                    hide_admin_jobs (bool): Whether to exclude admin jobs. Default is False.
                    clients_list (List[str]): List of client names to filter jobs. Default is [].
                    job_type_list (List[str]): List of job operation types. Default is [].
                    entity (Dict[str, Any]): Entity details to filter jobs (e.g., {"dataSourceId": 2575}).

        Returns:
            Dict[str, Any]: The constructed request JSON to be sent to the server.

        Example:
            >>> job_controller = JobController(commcell_object)
            >>> request_json = job_controller._get_jobs_request_json(
            ...     category='ACTIVE',
            ...     limit=10,
            ...     clients_list=['ClientA', 'ClientB'],
            ...     job_type_list=['Backup', 'Restore'],
            ...     entity={'dataSourceId': 2575}
            ... )
            >>> print(request_json)
            # The returned dictionary can be used to make a jobs API request.

        #ai-gen-doc
        """
        job_list_category = {
            'ALL': 0,
            'ACTIVE': 1,
            'FINISHED': 2
        }

        for client in options.get('clients_list', []):
            if not self._commcell_object.clients.has_client(client):
                raise SDKException('Job', '102', 'No client with name {0} exists.'.format(client))

        client_list = []
        for client in options.get('clients_list', []):
            try:
                _client_id = int(self._commcell_object.clients.all_clients[client.lower()]['id'])
            except KeyError:
                _client_id = int(self._commcell_object.clients.hidden_clients[client.lower()]['id'])
            client_list.append({"clientId": _client_id})

        request_json = {
            "scope": 1,
            "category": job_list_category[options.get('category', 'ALL')],
            "pagingConfig": {
                "sortDirection": 1,
                "offset": options.get('offset', 0),
                "sortField": "jobId",
                "limit": options.get('limit', 20)
            },
            "jobFilter": {
                "completedJobLookupTime": int(options.get('lookup_time', 5) * 60 * 60),
                "showAgedJobs": options.get('show_aged_jobs', False),
                "hideAdminJobs": options.get('hide_admin_jobs', False),
                "clientList": client_list,
                "jobTypeList": [
                    job_type for job_type in options.get('job_type_list', [])
                ]
            }
        }

        if "entity" in options:
            request_json['jobFilter']['entity'] = options.get("entity")

        return request_json

    def get_active_job_summary(self) -> Dict[str, int]:
        """Retrieve a summary of all active jobs in the Commcell.

        Returns:
            Dictionary containing counts of various active job states, such as suspended, running, queued, and anomalous jobs.

        Example:
            >>> job_controller = JobController(commcell_object)
            >>> summary = job_controller.get_active_job_summary()
            >>> print(summary)
            {
                "interruptPendingJobs": 0,
                "anomalousJobs": 1,
                "suspendedJobs": 368,
                "killPendingJobs": 0,
                "waitingJobs": 3,
                "killedJobs": 0,
                "suspendPendingJobs": 0,
                "runningJobs": 0,
                "queuedJobs": 0,
            }
            >>> print(f"Suspended jobs: {summary['suspendedJobs']}")
        #ai-gen-doc
        """
        return self._commcell_object.wrap_request(
            'POST', 'ACTIVE_JOBS_SUMMARY',
            req_kwargs={"payload": {"jobSummaryAggregationType":1}},
            error_check=False
        )

    def _get_jobs_list(self, **options: Any) -> Dict[str, Dict[str, Any]]:
        """Retrieve the list of jobs from the server with optional filtering.

        This method sends a request to the server to obtain job details. The returned dictionary contains 
        job information keyed by job ID. The level of detail in each job entry can be controlled using 
        the 'job_summary' option.

        Args:
            **options: Optional keyword arguments to customize the job query.
                - job_summary (str, optional): If set to 'full', returns the complete job summary for each job.
                  Otherwise, returns a filtered set of job attributes.

        Returns:
            Dictionary mapping job IDs to job details. Each value is either the full job summary or a 
            filtered dictionary of job attributes, depending on the 'job_summary' option.

        Raises:
            SDKException: If the server response is empty or unsuccessful.

        Example:
            >>> job_controller = JobController(...)
            >>> jobs = job_controller._get_jobs_list()
            >>> print(f"Retrieved {len(jobs)} jobs")
            >>> # To get full job summaries:
            >>> jobs_full = job_controller._get_jobs_list(job_summary='full')
            >>> print(jobs_full)
        #ai-gen-doc
        """
        request_json = self._get_jobs_request_json(**options)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ALL_JOBS'], request_json
        )

        jobs_dict = {}

        if flag:
            try:
                if response.json():
                    if 'jobs' in response.json():
                        all_jobs = response.json()['jobs']

                        for job in all_jobs:
                            if 'jobSummary' in job and job['jobSummary']['isVisible'] is True:

                                job_summary = job['jobSummary']
                                job_id = job_summary['jobId']

                                if options.get('job_summary', '').lower() == 'full':
                                    jobs_dict[job_id] = job_summary
                                else:
                                    status = job_summary['status']
                                    operation = job_summary.get('localizedOperationName', '')
                                    percent_complete = job_summary['percentComplete']
                                    backup_level = job_summary.get('backupLevelName')

                                    app_type = ''
                                    job_type = ''
                                    pending_reason = ''
                                    subclient_id = ''
                                    client_id = ''
                                    client_name = ''
                                    job_elapsed_time = 0
                                    job_start_time = 0

                                    if 'jobElapsedTime' in job_summary:
                                        job_elapsed_time = job_summary['jobElapsedTime']

                                    if 'jobStartTime' in job_summary:
                                        job_start_time = job_summary['jobStartTime']

                                    if 'appTypeName' in job_summary:
                                        app_type = job_summary['appTypeName']

                                    if 'jobType' in job_summary:
                                        job_type = job_summary['jobType']

                                    if 'pendingReason' in job_summary:
                                        pending_reason = job_summary['pendingReason']

                                    if 'subclient' in job_summary:
                                        job_subclient = job_summary['subclient']
                                        if 'subclientId' in job_subclient:
                                            subclient_id = job_subclient['subclientId']
                                        if 'clientId' in job_subclient:
                                            client_id = job_subclient['clientId']
                                        if 'clientName' in job_subclient:
                                            client_name = job_subclient['clientName']

                                    jobs_dict[job_id] = {
                                        'operation': operation,
                                        'status': status,
                                        'app_type': app_type,
                                        'job_type': job_type,
                                        'percent_complete': percent_complete,
                                        'pending_reason': pending_reason,
                                        'client_id': client_id,
                                        'client_name': client_name,
                                        'subclient_id': subclient_id,
                                        'backup_level': backup_level,
                                        'job_start_time': job_start_time,
                                        'job_elapsed_time': job_elapsed_time

                                    }

                    return jobs_dict

                else:
                    raise SDKException('Response', '102')

            except ValueError:
                raise SDKException('Response', '102', 'Please check the inputs.')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _modify_all_jobs(self, operation_type: Optional[str] = None) -> None:
        """Execute a request to suspend, resume, or kill all jobs on the CommServe.

        Args:
            operation_type: The operation to perform on all jobs. 
                Valid options are 'suspend', 'resume', or 'kill'.

        Raises:
            SDKException: If an invalid operation type is provided, if the API request fails,
                or if the server response is incorrect.

        Example:
            >>> job_controller = JobController(commcell_object)
            >>> job_controller._modify_all_jobs('suspend')  # Suspends all jobs
            >>> job_controller._modify_all_jobs('resume')   # Resumes all jobs
            >>> job_controller._modify_all_jobs('kill')     # Kills all jobs

        #ai-gen-doc
        """

        job_map = {
            'suspend': 'JOB_SUSPEND',
            'resume': 'JOB_RESUME',
            'kill': 'JOB_KILL'
        }

        if operation_type not in job_map:
            raise SDKException('Job', '102', 'Invalid input')

        request_json = {
            "JobManager_PerformMultiCellJobOpReq": {
                "jobOpReq": {
                    "operationType": job_map[operation_type]
                },
                "message": "ALL_JOBS",
                "operationDescription": "All jobs"
            }
        }

        response = self._commcell_object._qoperation_execute(request_json)

        if 'error' in response:
            error_code = response['error'].get('errorCode')
            if error_code != 0:
                if 'errLogMessage' in response['error']:
                    error_message = "Failed to {0} all jobs with error: [{1}]".format(
                        operation_type, response['error']['errLogMessage']
                    )

                    raise SDKException(
                        'Job',
                        '102',
                        'Error Code:"{0}"\nError Message: "{1}"'.format(error_code, error_message)
                    )
                else:
                    raise SDKException('Job',
                                       '102',
                                       "Failed to {0} all jobs".format(operation_type))
        else:
            raise SDKException('Response', '102')

    def all_jobs(self, client_name: Optional[str] = None, lookup_time: int = 5, job_filter: Optional[str] = None, **options: Any) -> Dict[str, Any]:
        """Retrieve all jobs executed on the Commcell within the specified lookup time.

        This method returns a dictionary of job IDs and their details, filtered by client name, job type, and other optional criteria.
        You can further refine the results using keyword arguments such as limit, offset, show_aged_job, hide_admin_jobs, clients_list, job_type_list, and job_summary.

        Args:
            client_name: Optional; name of the client to filter jobs for. If None, returns jobs for all clients.
            lookup_time: Number of hours to look back for executed jobs. Default is 5 hours.
            job_filter: Optional; comma-separated string of job types to filter (e.g., "Backup,Restore").
            **options: Additional keyword arguments to customize job retrieval.
                - limit (int): Maximum number of jobs to return. Default is 20.
                - offset (int): Starting index for job retrieval. Default is 0.
                - show_aged_job (bool): Whether to include aged jobs. Default is False.
                - hide_admin_jobs (bool): Whether to exclude admin jobs. Default is False.
                - clients_list (List[str]): List of client names to filter jobs.
                - job_type_list (List[str]): List of job operation types.
                - job_summary (str): 'basic' or 'full' summary. Default is 'basic'.

        Returns:
            Dictionary mapping job IDs to their details, matching the specified criteria.

        Raises:
            SDKException: If a client name is provided and no client exists with that name.

        Example:
            >>> job_controller = JobController()
            >>> jobs = job_controller.all_jobs(client_name="Server01", lookup_time=8, job_filter="Backup,Restore", limit=10)
            >>> print(f"Found {len(jobs)} jobs for Server01 in the last 8 hours")
            >>> # Access job details by job ID
            >>> for job_id, job_details in jobs.items():
            >>>     print(f"Job ID: {job_id}, Type: {job_details.get('type')}, Status: {job_details.get('status')}")
        #ai-gen-doc
        """
        options['category'] = 'ALL'
        options['lookup_time'] = lookup_time

        if job_filter:
            options['job_type_list'] = options.get('job_type_list', []) + job_filter.split(',')

        if client_name:
            options['clients_list'] = options.get('clients_list', []) + [client_name]

        return self._get_jobs_list(**options)

    def active_jobs(self, client_name: Optional[str] = None, lookup_time: int = 1, job_filter: Optional[str] = None, **options: Any) -> Dict[str, Any]:
        """Retrieve all active jobs currently being executed on the Commcell within the specified lookup time.

        This method returns a dictionary of active job IDs and their details, filtered by client name, job type, 
        and additional options. The lookup_time parameter specifies the number of hours to look back for active jobs.

        Args:
            client_name: Optional; name of the client to filter jobs for. If None, returns jobs for all clients.
            lookup_time: Number of hours to look back for active jobs. Default is 1.
            job_filter: Optional; comma-separated string of job types to filter (e.g., "Backup,Restore").
            **options: Additional keyword arguments to refine the job search. Supported options include:
                - limit (int): Maximum number of jobs to return. Default is 20.
                - offset (int): Starting index for job results. Default is 0.
                - show_aged_job (bool): Whether to include aged jobs. Default is False.
                - hide_admin_jobs (bool): Whether to exclude admin jobs. Default is False.
                - clients_list (List[str]): List of client names to filter jobs.
                - job_type_list (List[str]): List of job operation types.
                - job_summary (str): 'basic' or 'full' summary of jobs. Default is 'basic'.
                - entity (Dict[str, Any]): Entity details for associated jobs (e.g., {"dataSourceId": 2575}).

        Returns:
            Dictionary mapping job IDs to their details, matching the specified criteria.

        Raises:
            SDKException: If a client name is provided and no client exists with that name.

        Example:
            >>> job_controller = JobController()
            >>> # Get all active backup jobs for 'ClientA' in the last 2 hours
            >>> jobs = job_controller.active_jobs(client_name='ClientA', lookup_time=2, job_filter='Backup')
            >>> print(f"Active jobs: {jobs}")
            >>> # Get up to 10 active jobs with full summary
            >>> jobs = job_controller.active_jobs(limit=10, job_summary='full')
            >>> print(f"Job details: {jobs}")

        #ai-gen-doc
        """
        options['category'] = 'ACTIVE'
        options['lookup_time'] = lookup_time

        if job_filter:
            options['job_type_list'] = options.get('job_type_list', []) + job_filter.split(',')

        if client_name:
            options['clients_list'] = options.get('clients_list', []) + [client_name]

        return self._get_jobs_list(**options)

    def finished_jobs(self, client_name: Optional[str] = None, lookup_time: int = 24, job_filter: Optional[str] = None, **options: Any) -> Dict[str, Any]:
        """Retrieve all finished jobs from the Commcell within the specified lookup time.

        This method returns a dictionary of finished jobs, filtered by client name, job type, and other optional criteria.
        The lookup_time parameter specifies the number of hours to look back for finished jobs.
        Additional filtering options can be provided via keyword arguments.

        Args:
            client_name: Optional; name of the client to filter jobs for. If None, jobs for all clients are returned.
            lookup_time: Number of hours to look back for finished jobs. Default is 24.
            job_filter: Optional; comma-separated string of job types to filter (e.g., "Backup,Restore,AUXCOPY").
            **options: Additional keyword arguments for advanced filtering, such as:
                - limit (int): Maximum number of jobs to return (default: 20).
                - offset (int): Starting index for job results (default: 0).
                - show_aged_job (bool): Whether to include aged jobs (default: False).
                - hide_admin_jobs (bool): Whether to exclude admin jobs (default: False).
                - clients_list (List[str]): List of client names to filter jobs.
                - job_type_list (List[str]): List of job operation types.
                - job_summary (str): 'basic' or 'full' job summary (default: 'basic').
                - entity (Dict[str, Any]): Entity details for associated jobs (e.g., {"dataSourceId": 2575}).

        Returns:
            Dictionary mapping job IDs to their details, matching the specified criteria.

        Raises:
            SDKException: If a client name is provided and no client exists with that name.

        Example:
            >>> job_controller = JobController()
            >>> finished = job_controller.finished_jobs(client_name="ClientA", lookup_time=12, job_filter="Backup,Restore", limit=10)
            >>> for job_id, job_details in finished.items():
            ...     print(f"Job ID: {job_id}, Type: {job_details.get('type')}, Status: {job_details.get('status')}")
        #ai-gen-doc
        """
        options['category'] = 'FINISHED'
        options['lookup_time'] = lookup_time

        if job_filter:
            options['job_type_list'] = options.get('job_type_list', []) + job_filter.split(',')

        if client_name:
            options['clients_list'] = options.get('clients_list', []) + [client_name]

        return self._get_jobs_list(**options)

    def suspend_all_jobs(self) -> None:
        """Suspend all active jobs on the CommServe server.

        This method initiates a suspend operation for every running job on the CommServe,
        pausing their execution until resumed or cancelled.

        Example:
            >>> job_controller = JobController()
            >>> job_controller.suspend_all_jobs()
            >>> print("All jobs have been suspended on the CommServe.")
        #ai-gen-doc
        """
        self._modify_all_jobs('suspend')

    def resume_all_jobs(self) -> None:
        """Resume all jobs on the CommServe server.

        This method resumes all paused or suspended jobs managed by the CommServe.

        Example:
            >>> job_controller = JobController()
            >>> job_controller.resume_all_jobs()
            >>> print("All jobs have been resumed.")

        #ai-gen-doc
        """
        self._modify_all_jobs('resume')

    def kill_all_jobs(self) -> None:
        """Terminate all active jobs on the CommServe server.

        This method sends a command to kill all currently running jobs on the CommServe.
        Use with caution, as this will stop all ongoing operations.

        Example:
            >>> job_controller = JobController()
            >>> job_controller.kill_all_jobs()
            >>> print("All jobs have been terminated.")

        #ai-gen-doc
        """
        self._modify_all_jobs('kill')

    def get(self, job_id: int) -> 'Job':
        """Retrieve the Job object for the specified job ID.

        Args:
            job_id: The unique identifier of the job to retrieve.

        Returns:
            Job: An instance of the Job class corresponding to the given job ID.

        Raises:
            SDKException: If no job with the specified job ID exists.

        Example:
            >>> job_controller = JobController(commcell_object)
            >>> job = job_controller.get(12345)
            >>> print(f"Job ID: {job.job_id}")
            >>> # The returned Job object can be used for further job operations

        #ai-gen-doc
        """
        return Job(self._commcell_object, job_id)


class JobManagement(object):
    """
    Comprehensive class for managing and configuring job operations within a CommCell environment.

    The JobManagement class provides a robust interface for controlling various aspects of job execution,
    prioritization, error handling, and operational settings. It enables administrators to fine-tune job
    management parameters, set and retrieve general, priority, restart, and update settings, and manage
    job behaviors through a variety of property-based configurations.

    Key Features:
        - Initialization with a CommCell object for context-aware job management
        - Refreshing job management settings to ensure up-to-date configurations
        - Setting and retrieving general, priority, restart, and update settings for jobs
        - Fine-grained control over job priority precedence and operational intervals
        - Configurable error rules and job error thresholds
        - Management of job queuing, throttling, and multiplexing for various agents and job types
        - Control over job behaviors such as preemption, activity windows, and backup/restore operations
        - Property-based access to all major job management settings for easy integration and automation

    This class is intended for use in environments where job execution and management require detailed
    configuration and monitoring to ensure optimal performance and reliability.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize the JobManagement instance for managing job management settings.

        Args:
            commcell_object: Instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> job_mgmt = JobManagement(commcell)
            >>> # The JobManagement object can now be used to manage job settings

        #ai-gen-doc
        """
        self._comcell = commcell_object
        self._service = commcell_object._services.get('JOB_MANAGEMENT_SETTINGS')
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._error_rules = None
        self.refresh()

    @property
    def error_rules(self) -> '_ErrorRule':
        """Get the _ErrorRule instance associated with this JobManagement object.

        Returns:
            _ErrorRule: An instance for managing error rules related to job management.

        Example:
            >>> job_mgmt = JobManagement(commcell_object)
            >>> error_rules = job_mgmt.error_rules  # Use dot notation for property access
            >>> print(f"Error rules object: {error_rules}")
            >>> # The returned _ErrorRule object can be used to manage job error rules

        #ai-gen-doc
        """
        if not self._error_rules:
            self._error_rules = _ErrorRule(self._comcell)
        return self._error_rules

    def _set_jobmanagement_settings(self) -> None:
        """Set job management settings on the server.

        This method sends a POST request to the server to update job management settings 
        using the current configuration. If the server returns an error, an SDKException 
        is raised with the relevant error message.

        Raises:
            SDKException: If the server response indicates an error or if the inputs are invalid.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> job_mgmt._set_jobmanagement_settings()
            >>> print("Job management settings updated successfully")
            # If an error occurs, SDKException will be raised with details.

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request(method='POST', url=self._service,
                                                           payload=self._settings_dict)
        if flag:
            if response and response.json():
                if response.json().get('errorCode', 0) != 0:
                    raise SDKException('Job', '102', 'Failed to set job management properties. \nError: {0}'.format(
                        response.json().get('errorMessage', '')))
                self.refresh()
        else:
            raise SDKException('Response', '101', response.json()["errorMessage"])

    def _get_jobmanagement_settings(self) -> None:
        """Retrieve job management settings from the server and update internal state.

        This method sends a GET request to the server to fetch job management settings. 
        The settings are parsed and stored in internal attributes for restart, priority, 
        general, and update settings. If the response is empty or indicates an error, 
        an SDKException is raised.

        Raises:
            SDKException: If the server response is empty, unsuccessful, or contains an error code.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> job_mgmt._get_jobmanagement_settings()
            >>> # After execution, job management settings are available in internal attributes
            >>> # e.g., job_mgmt._restart_settings, job_mgmt._priority_settings

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(method='GET', url=self._service)
        if flag:
            if response and response.json():
                self._settings_dict = response.json()
                if self._settings_dict.get('errorCode', 0) != 0:
                    raise SDKException('Job', '102', 'Failed to get job management properties. \nError: {0}'.format(
                        self._settings_dict.get('errorMessage', '')))
                if 'jobManagementSettings' in self._settings_dict:
                    self._restart_settings = {'jobRestartSettings': self._settings_dict.get(
                        'jobManagementSettings').get('jobRestartSettings', {})}
                    self._priority_settings = {'jobPrioritySettings': self._settings_dict.get(
                        'jobManagementSettings').get('jobPrioritySettings', {})}
                    self._general_settings = {'generalSettings': self._settings_dict.get(
                        'jobManagementSettings').get('generalSettings', {})}
                    self._update_settings = {'jobUpdatesSettings': self._settings_dict.get(
                        'jobManagementSettings').get('jobUpdatesSettings', {})}
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._comcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Reload all job management settings from the Commcell.

        This method clears cached job management settings and retrieves the latest configuration 
        by calling the internal method. Use this to ensure you are working with up-to-date 
        job management parameters.

        Example:
            >>> job_mgmt = JobManagement(commcell_object)
            >>> job_mgmt.refresh()  # Refreshes job management settings
            >>> print("Job management settings reloaded successfully")

        #ai-gen-doc
        """
        self._restart_settings = None
        self._general_settings = None
        self._update_settings = None
        self._priority_settings = None
        self._get_jobmanagement_settings()

    def set_general_settings(self, settings: Dict[str, Any]) -> None:
        """Set general job management settings using the provided configuration dictionary.

        This method updates the general job management settings with the specified key-value pairs.
        Dedicated setters and getters are available for individual settings, but this method allows
        batch updating of multiple settings at once.

        Args:
            settings: Dictionary containing general job management settings to update. 
                Supported keys include:
                    - "allowRunningJobsToCompletePastOperationWindow": bool
                    - "jobAliveCheckIntervalInMinutes": int
                    - "queueScheduledJobs": bool
                    - "enableJobThrottleAtClientLevel": bool
                    - "enableMultiplexingForDBAgents": bool
                    - "queueJobsIfConflictingJobsActive": bool
                    - "queueJobsIfActivityDisabled": bool
                    - "backupsPreemptsAuxilaryCopy": bool
                    - "restorePreemptsOtherJobs": bool
                    - "enableMultiplexingForOracle": bool
                    - "jobStreamHighWaterMarkLevel": int
                    - "backupsPreemptsOtherBackups": bool
                    - "doNotStartBackupsOnDisabledClient": bool

        Raises:
            SDKException: If the input is not a valid dictionary.

        Example:
            >>> job_mgmt = JobManagement()
            >>> settings = {
            ...     "allowRunningJobsToCompletePastOperationWindow": False,
            ...     "jobAliveCheckIntervalInMinutes": 10,
            ...     "queueScheduledJobs": True
            ... }
            >>> job_mgmt.set_general_settings(settings)
            >>> # The general job management settings are now updated

        #ai-gen-doc
        """
        if isinstance(settings, dict):
            self._general_settings.get('generalSettings').update(settings)
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    def set_priority_settings(self, settings: List[Dict[str, Any]]) -> None:
        """Set priority settings for jobs and agent types.

        This method updates the priority configuration for job types and agent types based on the provided settings.
        Each setting should be a dictionary specifying the type of operation, combined priority, and either the job type name or agent type name.

        Args:
            settings: A list of dictionaries, each containing priority settings. The format should be:
                [
                    {
                        "type_of_operation": 1,
                        "combinedPriority": 10,
                        "jobTypeName": "Information Management"
                    },
                    {
                        "type_of_operation": 2,
                        "combinedPriority": 10,
                        "appTypeName": "Windows File System"
                    },
                    {
                        "type_of_operation": 1,
                        "combinedPriority": 10,
                        "jobTypeName": "Auxiliary Copy"
                    }
                ]
                - For job type priority, set "type_of_operation" to 1 and specify "jobTypeName".
                - For agent type priority, set "type_of_operation" to 2 and specify "appTypeName".

        Raises:
            SDKException: If the input is not a valid list of dictionaries.

        Example:
            >>> job_mgmt = JobManagement()
            >>> settings = [
            ...     {"type_of_operation": 1, "combinedPriority": 10, "jobTypeName": "Information Management"},
            ...     {"type_of_operation": 2, "combinedPriority": 10, "appTypeName": "Windows File System"}
            ... ]
            >>> job_mgmt.set_priority_settings(settings)
            >>> print("Priority settings updated successfully")

        #ai-gen-doc
        """
        if isinstance(settings, list):
            for job in settings:
                if job["type_of_operation"] == 1:
                    for job_type in self._priority_settings['jobPrioritySettings']['jobTypePriorityList']:
                        if job_type['jobTypeName'] == job.get("jobTypeName"):
                            job.pop("jobTypeName")
                            job.pop("type_of_operation")
                            job_type.update(job)
                            break
                elif job["type_of_operation"] == 2:
                    for job_type in self._priority_settings['jobPrioritySettings']['agentTypePriorityList']:
                        if job_type['agentTypeEntity']['appTypeName'] == job.get("appTypeName"):
                            job.pop("appTypeName")
                            job.pop("type_of_operation")
                            job_type.update(job)
                            break
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    def set_restart_settings(self, settings: List[Dict[str, Any]]) -> None:
        """Set restart settings for jobs based on the provided configuration.

        Args:
            settings: A list of dictionaries, each containing restart settings for a specific job type.
                Each dictionary should include keys such as:
                    - "killRunningJobWhenTotalRunningTimeExpires": bool
                    - "maxRestarts": int
                    - "enableTotalRunningTime": bool
                    - "restartable": bool
                    - "jobTypeName": str
                    - "restartIntervalInMinutes": int
                    - "preemptable": bool
                    - "totalRunningTime": int
                    - "jobType": int

        Raises:
            SDKException: If the input is not a valid list of dictionaries.

        Example:
            >>> job_settings = [
            ...     {
            ...         "killRunningJobWhenTotalRunningTimeExpires": False,
            ...         "maxRestarts": 10,
            ...         "enableTotalRunningTime": False,
            ...         "restartable": False,
            ...         "jobTypeName": "File System and Indexing Based (Data Protection)",
            ...         "restartIntervalInMinutes": 20,
            ...         "preemptable": True,
            ...         "totalRunningTime": 21600,
            ...         "jobType": 6
            ...     },
            ...     {
            ...         "killRunningJobWhenTotalRunningTimeExpires": False,
            ...         "maxRestarts": 144,
            ...         "enableTotalRunningTime": False,
            ...         "restartable": False,
            ...         "jobTypeName": "File System and Indexing Based (Data Recovery)",
            ...         "restartIntervalInMinutes": 20,
            ...         "preemptable": False,
            ...         "totalRunningTime": 21600,
            ...         "jobType": 7
            ...     }
            ... ]
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.set_restart_settings(job_settings)
            >>> print("Restart settings updated successfully.")

        #ai-gen-doc
        """

        if isinstance(settings, list):
            for job in settings:
                target = {'target': job_type for job_type in
                          self._restart_settings['jobRestartSettings']['jobTypeRestartSettingList']
                          if job_type['jobTypeName'] == job.get("jobTypeName")}
                target.get('target').update(job)
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    def set_update_settings(self, settings: List[Dict[str, Any]]) -> None:
        """Set update settings for jobs using a list of configuration dictionaries.

        Args:
            settings: A list of dictionaries, each specifying update settings for a job type.
                Each dictionary should have the following format:
                    {
                        "appTypeName": str,                # Name of the application type (e.g., "Windows File System")
                        "recoveryTimeInMinutes": int,      # Recovery time in minutes
                        "protectionTimeInMinutes": int     # Protection time in minutes
                    }

        Raises:
            SDKException: If the input is not a list of dictionaries.

        Example:
            >>> job_settings = [
            ...     {
            ...         "appTypeName": "Windows File System",
            ...         "recoveryTimeInMinutes": 20,
            ...         "protectionTimeInMinutes": 20
            ...     },
            ...     {
            ...         "appTypeName": "Windows XP 64-bit File System",
            ...         "recoveryTimeInMinutes": 20,
            ...         "protectionTimeInMinutes": 20
            ...     }
            ... ]
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.set_update_settings(job_settings)
            >>> print("Job update settings applied successfully")
        #ai-gen-doc
        """

        if isinstance(settings, list):
            for job in settings:
                for job_type in self._update_settings['jobUpdatesSettings']['agentTypeJobUpdateIntervalList']:
                    if job_type['agentTypeEntity']['appTypeName'] == job.get("appTypeName"):
                        job.pop("appTypeName")
                        job_type.update(job)
                        break
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    @property
    def job_priority_precedence(self) -> str:
        """Get the job priority precedence type set for job management.

        Returns:
            The type of job priority precedence as a string, such as "client" or "agentType".

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> precedence = job_mgmt.job_priority_precedence  # Use dot notation for properties
            >>> print(f"Job priority precedence: {precedence}")
            >>> # Output could be "client" or "agentType" depending on configuration

        #ai-gen-doc
        """

        available_priorities = {
            1: "client",
            2: "agentType"
        }
        return available_priorities.get(self._priority_settings["jobPrioritySettings"]["priorityPrecedence"])

    @job_priority_precedence.setter
    def job_priority_precedence(self, priority_type: str) -> None:
        """Set the job priority precedence for job management.

        Args:
            priority_type: The type of priority to be set. Must be one of:
                - "client": Prioritize jobs based on client.
                - "agentType": Prioritize jobs based on agent type.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.job_priority_precedence = "client"      # Set precedence to client
            >>> job_mgmt.job_priority_precedence = "agentType"   # Set precedence to agent type

        #ai-gen-doc
        """
        if isinstance(priority_type, str):
            available_priorities = {
                "client": 1,
                "agentType": 2
            }
            self._priority_settings["jobPrioritySettings"]["priorityPrecedence"] = available_priorities[priority_type]
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    @property
    def start_phase_retry_interval(self) -> int:
        """Get the start phase retry interval in minutes for job restarts.

        Returns:
            The interval in minutes as an integer.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> interval = job_mgmt.start_phase_retry_interval  # Use dot notation for property
            >>> print(f"Start phase retry interval: {interval} minutes")
        #ai-gen-doc
        """
        return self._restart_settings["jobRestartSettings"]["startPhaseRetryIntervalInMinutes"]

    @start_phase_retry_interval.setter
    def start_phase_retry_interval(self, minutes: int) -> None:
        """Set the start phase retry interval for jobs in minutes.

        Args:
            minutes: The number of minutes to set for the start phase retry interval.

        Raises:
            SDKException: If the input is not of type int.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.start_phase_retry_interval = 15  # Sets retry interval to 15 minutes
            >>> # If a non-integer value is provided, SDKException will be raised

        #ai-gen-doc
        """

        if isinstance(minutes, int):
            self._restart_settings["jobRestartSettings"]["startPhaseRetryIntervalInMinutes"] = minutes
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    @property
    def state_update_interval_for_continuous_data_replicator(self) -> int:
        """Get the state update interval for continuous data replicator jobs in minutes.

        Returns:
            The interval, in minutes, at which state updates are performed for continuous data replicator jobs.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> interval = job_mgmt.state_update_interval_for_continuous_data_replicator
            >>> print(f"State update interval: {interval} minutes")
        #ai-gen-doc
        """
        return self._update_settings["jobUpdatesSettings"]["stateUpdateIntervalForContinuousDataReplicator"]

    @state_update_interval_for_continuous_data_replicator.setter
    def state_update_interval_for_continuous_data_replicator(self, minutes: int) -> None:
        """Set the state update interval for continuous data replicator jobs.

        Args:
            minutes: The interval in minutes to set for state updates.

        Raises:
            SDKException: If the provided value for minutes is not an integer.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.state_update_interval_for_continuous_data_replicator = 15
            >>> # The state update interval for continuous data replicator jobs is now set to 15 minutes.

        #ai-gen-doc
        """
        if isinstance(minutes, int):
            self._update_settings["jobUpdatesSettings"]["stateUpdateIntervalForContinuousDataReplicator"] = minutes
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    @property
    def allow_running_jobs_to_complete_past_operation_window(self) -> bool:
        """Indicate whether running jobs are allowed to complete past the operation window.

        Returns:
            True if the option to allow running jobs to complete past the operation window is enabled; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> if job_mgmt.allow_running_jobs_to_complete_past_operation_window:
            ...     print("Jobs can continue past the operation window.")
            ... else:
            ...     print("Jobs will be stopped at the end of the operation window.")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("allowRunningJobsToCompletePastOperationWindow")

    @allow_running_jobs_to_complete_past_operation_window.setter
    def allow_running_jobs_to_complete_past_operation_window(self, flag: bool) -> None:
        """Enable or disable the option to allow running jobs to complete past the operation window.

        Args:
            flag: Set to True to allow running jobs to complete past the operation window, or False to prevent it.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.allow_running_jobs_to_complete_past_operation_window = True  # Enable completion past window
            >>> job_mgmt.allow_running_jobs_to_complete_past_operation_window = False # Disable completion past window

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "allowRunningJobsToCompletePastOperationWindow": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def job_alive_check_interval_in_minutes(self) -> int:
        """Get the job alive check interval in minutes.

        Returns:
            The interval, in minutes, used to check if a job is still alive.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> interval = job_mgmt.job_alive_check_interval_in_minutes
            >>> print(f"Job alive check interval: {interval} minutes")
        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("jobAliveCheckIntervalInMinutes")

    @job_alive_check_interval_in_minutes.setter
    def job_alive_check_interval_in_minutes(self, minutes: int) -> None:
        """Set the job alive check interval in minutes.

        Args:
            minutes: The interval in minutes to be set for job alive checks.

        Raises:
            SDKException: If the input is not of type int.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.job_alive_check_interval_in_minutes = 15  # Set interval to 15 minutes
            >>> # The job alive check interval is now updated

        #ai-gen-doc
        """
        if isinstance(minutes, int):
            settings = {
                "jobAliveCheckIntervalInMinutes": minutes
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def queue_scheduled_jobs(self) -> bool:
        """Indicate whether the option to queue scheduled jobs is enabled.

        Returns:
            True if the queue scheduled jobs option is enabled; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> is_queued = job_mgmt.queue_scheduled_jobs  # Use dot notation for property
            >>> print(f"Queue scheduled jobs enabled: {is_queued}")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("queueScheduledJobs")

    @queue_scheduled_jobs.setter
    def queue_scheduled_jobs(self, flag: bool) -> None:
        """Enable or disable queuing of scheduled jobs.

        Args:
            flag: Boolean value indicating whether to enable (True) or disable (False) queuing of scheduled jobs.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> job_mgmt.queue_scheduled_jobs = True  # Enable queuing of scheduled jobs
            >>> job_mgmt.queue_scheduled_jobs = False # Disable queuing of scheduled jobs

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "queueScheduledJobs": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def enable_job_throttle_at_client_level(self) -> bool:
        """Indicate whether job throttling is enabled at the client level.

        Returns:
            True if job throttling is enabled for clients, False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> is_throttle_enabled = job_mgmt.enable_job_throttle_at_client_level
            >>> print(f"Job throttle at client level enabled: {is_throttle_enabled}")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("enableJobThrottleAtClientLevel")

    @enable_job_throttle_at_client_level.setter
    def enable_job_throttle_at_client_level(self, flag: bool) -> None:
        """Enable or disable job throttling at the client level.

        Args:
            flag: Set to True to enable job throttle at the client level, or False to disable it.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> job_mgmt.enable_job_throttle_at_client_level = True  # Enable job throttle
            >>> job_mgmt.enable_job_throttle_at_client_level = False # Disable job throttle

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "enableJobThrottleAtClientLevel": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def enable_multiplexing_for_db_agents(self) -> bool:
        """Indicate whether multiplexing is enabled for database agents.

        Returns:
            True if multiplexing is enabled for database agents, False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> is_enabled = job_mgmt.enable_multiplexing_for_db_agents  # Use dot notation for property
            >>> print(f"Multiplexing enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("enableMultiplexingForDBAgents")

    @enable_multiplexing_for_db_agents.setter
    def enable_multiplexing_for_db_agents(self, flag: bool) -> None:
        """Enable or disable multiplexing for database agents.

        Args:
            flag: Boolean value indicating whether to enable (True) or disable (False) multiplexing for DB agents.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.enable_multiplexing_for_db_agents = True  # Enable multiplexing
            >>> job_mgmt.enable_multiplexing_for_db_agents = False # Disable multiplexing

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "enableMultiplexingForDBAgents": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def queue_jobs_if_conflicting_jobs_active(self) -> bool:
        """Indicate whether jobs are queued if conflicting jobs are active.

        Returns:
            True if the option to queue jobs when conflicting jobs are active is enabled; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> if job_mgmt.queue_jobs_if_conflicting_jobs_active:
            ...     print("Jobs will be queued when conflicts are detected.")
            ... else:
            ...     print("Jobs will not be queued during conflicts.")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("queueJobsIfConflictingJobsActive")

    @queue_jobs_if_conflicting_jobs_active.setter
    def queue_jobs_if_conflicting_jobs_active(self, flag: bool) -> None:
        """Enable or disable queuing of jobs when conflicting jobs are active.

        Args:
            flag: Boolean value indicating whether to queue jobs if conflicting jobs are active.
                - True: Enable queuing of jobs.
                - False: Disable queuing of jobs.

        Raises:
            SDKException: If the input flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.queue_jobs_if_conflicting_jobs_active = True  # Enable queuing
            >>> job_mgmt.queue_jobs_if_conflicting_jobs_active = False # Disable queuing

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "queueJobsIfConflictingJobsActive": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def queue_jobs_if_activity_disabled(self) -> bool:
        """Indicate whether jobs are queued when activity is disabled.

        Returns:
            True if the option to queue jobs when activity is disabled is enabled; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> if job_mgmt.queue_jobs_if_activity_disabled:
            ...     print("Jobs will be queued when activity is disabled.")
            ... else:
            ...     print("Jobs will not be queued when activity is disabled.")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("queueJobsIfActivityDisabled")

    @queue_jobs_if_activity_disabled.setter
    def queue_jobs_if_activity_disabled(self, flag: bool) -> None:
        """Enable or disable queuing of jobs when activity is disabled.

        Args:
            flag: Boolean value indicating whether to queue jobs if activity is disabled.
                - True: Jobs will be queued when activity is disabled.
                - False: Jobs will not be queued.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.queue_jobs_if_activity_disabled = True  # Enable queuing
            >>> job_mgmt.queue_jobs_if_activity_disabled = False # Disable queuing

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "queueJobsIfActivityDisabled": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def backups_preempts_auxilary_copy(self) -> bool:
        """Indicate whether backup jobs can preempt auxiliary copy operations.

        Returns:
            True if the "Backups Preempts Auxiliary Copy" option is enabled; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> if job_mgmt.backups_preempts_auxilary_copy:
            ...     print("Backup jobs will preempt auxiliary copy operations.")
            ... else:
            ...     print("Backup jobs will not preempt auxiliary copy operations.")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("backupsPreemptsAuxilaryCopy")

    @backups_preempts_auxilary_copy.setter
    def backups_preempts_auxilary_copy(self, flag: bool) -> None:
        """Enable or disable the 'backups preempts auxiliary copy' setting.

        Args:
            flag: Boolean value to set the option. 
                - True enables backups to preempt auxiliary copy operations.
                - False disables this behavior.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> job_mgmt.backups_preempts_auxilary_copy = True  # Enable preemption
            >>> job_mgmt.backups_preempts_auxilary_copy = False # Disable preemption

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "backupsPreemptsAuxilaryCopy": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def restore_preempts_other_jobs(self) -> bool:
        """Indicate whether the 'Restore Preempts Other Jobs' option is enabled.

        Returns:
            True if the restore operation is configured to preempt other jobs; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> if job_mgmt.restore_preempts_other_jobs:
            ...     print("Restore jobs will preempt other running jobs.")
            ... else:
            ...     print("Restore jobs will not preempt other jobs.")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("restorePreemptsOtherJobs")

    @restore_preempts_other_jobs.setter
    def restore_preempts_other_jobs(self, flag: bool) -> None:
        """Enable or disable the 'restore preempts other jobs' setting.

        Args:
            flag: Boolean value indicating whether restore operations should preempt other jobs.
                - True: Restore jobs will preempt other running jobs.
                - False: Restore jobs will not preempt other jobs.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> job_mgmt.restore_preempts_other_jobs = True  # Enable preemption
            >>> job_mgmt.restore_preempts_other_jobs = False # Disable preemption

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "restorePreemptsOtherJobs": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def enable_multiplexing_for_oracle(self) -> bool:
        """Indicate whether multiplexing is enabled for Oracle jobs.

        Returns:
            True if multiplexing is enabled for Oracle jobs, False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> is_enabled = job_mgmt.enable_multiplexing_for_oracle  # Use dot notation for property
            >>> print(f"Multiplexing enabled for Oracle: {is_enabled}")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("enableMultiplexingForOracle")

    @enable_multiplexing_for_oracle.setter
    def enable_multiplexing_for_oracle(self, flag: bool) -> None:
        """Enable or disable multiplexing for Oracle jobs.

        Args:
            flag: Boolean value to set multiplexing. 
                - True to enable multiplexing for Oracle jobs.
                - False to disable multiplexing.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.enable_multiplexing_for_oracle = True  # Enable multiplexing
            >>> job_mgmt.enable_multiplexing_for_oracle = False # Disable multiplexing

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "enableMultiplexingForOracle": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def job_stream_high_water_mark_level(self) -> int:
        """Get the job stream high water mark level for job management.

        This property retrieves the configured high water mark level, which determines 
        the maximum number of concurrent job streams allowed.

        Returns:
            The job stream high water mark level as an integer.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> high_water_mark = job_mgmt.job_stream_high_water_mark_level
            >>> print(f"High water mark level: {high_water_mark}")
        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("jobStreamHighWaterMarkLevel")

    @job_stream_high_water_mark_level.setter
    def job_stream_high_water_mark_level(self, level: int) -> None:
        """Set the job stream high water mark level.

        This property setter configures the maximum number of jobs that can be performed concurrently 
        in a job stream. The value must be an integer.

        Args:
            level: The number of jobs to be performed at a time (as an integer).

        Raises:
            SDKException: If the provided level is not an integer.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.job_stream_high_water_mark_level = 5  # Set to allow 5 concurrent jobs
            >>> # The job stream high water mark level is now set to 5

        #ai-gen-doc
        """
        if isinstance(level, int):
            settings = {
                "jobStreamHighWaterMarkLevel": level
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def backups_preempts_other_backups(self) -> bool:
        """Indicate whether backup jobs can preempt other backup jobs.

        Returns:
            True if the "Backups Preempts Other Backups" option is enabled; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> can_preempt = job_mgmt.backups_preempts_other_backups
            >>> print(f"Backups can preempt other backups: {can_preempt}")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("backupsPreemptsOtherBackups")

    @backups_preempts_other_backups.setter
    def backups_preempts_other_backups(self, flag: bool) -> None:
        """Enable or disable the setting for backups to preempt other backups.

        Args:
            flag: Boolean value indicating whether backups should preempt other backups.
                - True: Enable preemption of backups.
                - False: Disable preemption of backups.

        Raises:
            SDKException: If the input flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> job_mgmt.backups_preempts_other_backups = True  # Enable preemption
            >>> job_mgmt.backups_preempts_other_backups = False # Disable preemption

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "backupsPreemptsOtherBackups": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def do_not_start_backups_on_disabled_client(self) -> bool:
        """Indicate whether backups are prevented from starting on disabled clients.

        Returns:
            True if the option to not start backups on disabled clients is enabled; False otherwise.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> if job_mgmt.do_not_start_backups_on_disabled_client:
            ...     print("Backups will not start on disabled clients.")
            ... else:
            ...     print("Backups may start on disabled clients.")

        #ai-gen-doc
        """
        return self._general_settings.get('generalSettings').get("doNotStartBackupsOnDisabledClient")

    @do_not_start_backups_on_disabled_client.setter
    def do_not_start_backups_on_disabled_client(self, flag: bool) -> None:
        """Enable or disable the option to prevent backups on disabled clients.

        Args:
            flag: Boolean value indicating whether to prevent backups on disabled clients.
                - True: Backups will not start on disabled clients.
                - False: Backups may start on disabled clients.

        Raises:
            SDKException: If the provided flag is not a boolean value.

        Example:
            >>> job_mgmt = JobManagement()
            >>> job_mgmt.do_not_start_backups_on_disabled_client = True  # Prevent backups on disabled clients
            >>> job_mgmt.do_not_start_backups_on_disabled_client = False # Allow backups on disabled clients

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            settings = {
                "doNotStartBackupsOnDisabledClient": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    def get_restart_setting(self, jobtype: str) -> Dict[str, Any]:
        """Retrieve restart settings for a specific job type.

        Args:
            jobtype: The name of the job type for which to obtain restart settings.
                Available job types include (but are not limited to):
                    - "Disaster Recovery backup"
                    - "Auxiliary Copy"
                    - "Data Aging"
                    - "Download/Copy Updates"
                    - "Offline Content Indexing"
                    - "Information Management"
                    - "File System and Indexing Based (Data Protection)"
                    - "File System and Indexing Based (Data Recovery)"
                    - "Exchange DB (Data Protection)"
                    - "Exchange DB (Data Recovery)"
                    - "Informix DB (Data Protection)"
                    - "Informix DB (Data Recovery)"
                    - "Lotus Notes DB (Data Protection)"
                    - "Lotus Notes DB (Data Recovery)"
                    - "Oracle DB (Data Protection)"
                    - "Oracle DB (Data Recovery)"
                    - "SQL DB (Data Protection)"
                    - "SQL DB (Data Recovery)"
                    - "MYSQL (Data Protection)"
                    - "MYSQL (Data Recovery)"
                    - "Sybase DB (Data Protection)"
                    - "Sybase DB (Data Recovery)"
                    - "DB2 (Data Protection)"
                    - "DB2 (Data Recovery)"
                    - "CDR (Data Management)"
                    - "Media Refresh"
                    - "Documentum (Data Protection)"
                    - "Documentum (Data Recovery)"
                    - "SAP for Oracle (Data Protection)"
                    - "SAP for Oracle (Data Recovery)"
                    - "PostgreSQL (Data Protection)"
                    - "PostgreSQL (Data Recovery)"
                    - "Other (Data Protection)"
                    - "Other (Data Recovery)"
                    - "Workflow"
                    - "DeDup DB Reconstruction"
                    - "CommCell Migration Export"
                    - "CommCell Migration Import"
                    - "Install Software"
                    - "Uninstall Software"
                    - "Data Verification"
                    - "Big Data Apps (Data Protection)"
                    - "Big Data Apps (Data Recovery)"
                    - "Cloud Apps (Data Protection)"
                    - "Cloud Apps (Data Recovery)"
                    - "Virtual Server (Data Protection)"
                    - "Virtual Server (Data Recovery)"
                    - "SAP for Hana (Data Protection)"
                    - "SAP for Hana (Data Recovery)"

        Returns:
            Dictionary containing the restart settings for the specified job type, for example:
                {
                    "jobTypeName": "File System and Indexing Based (Data Protection)",
                    "restartable": True,
                    "maxRestarts": 10,
                    "restartIntervalInMinutes": 20,
                    "enableTotalRunningTime": False,
                    "totalRunningTime": 25200,
                    "killRunningJobWhenTotalRunningTimeExpires": False,
                    "preemptable": True,
                }

        Raises:
            SDKException: If the input jobtype is not a valid string.

        Example:
            >>> job_mgr = JobManagement()
            >>> settings = job_mgr.get_restart_setting("File System and Indexing Based (Data Protection)")
            >>> print(settings["restartable"])
            True

        #ai-gen-doc
        """
        if isinstance(jobtype, str):
            for job_type in self._restart_settings['jobRestartSettings']['jobTypeRestartSettingList']:
                if job_type['jobTypeName'] == jobtype:
                    settings = copy.deepcopy(job_type)
                    return settings
        else:
            raise SDKException('Job', '108')

    def get_priority_setting(self, jobtype: str) -> Dict[str, Any]:
        """Retrieve the priority settings associated with a specific job type or application type.

        Args:
            jobtype: The name of the job type or application type for which to obtain priority settings.
                Available job type names include:
                    "Information Management", "Auxiliary Copy", "Media Refresh", "Data Verification",
                    "Persistent Recovery", "Synth Full"
                Available application type names include:
                    "Windows File System", "Active Directory", "Exchange Mailbox", "Oracle Database",
                    "SQL Server", "Linux File System", "SAP HANA", "Cloud Apps", and many others.

        Returns:
            Dictionary containing the priority settings for the specified job type or application type.
            Example for job type:
                {
                    "jobTypeName": "Information Management",
                    "combinedPriority": 0,
                    "type_of_operation": 1
                }
            Example for application type:
                {
                    "appTypeName": "Windows File System",
                    "combinedPriority": 6,
                    "type_of_operation": 2
                }

        Raises:
            SDKException: If the input jobtype is not a valid string or does not match any known type.

        Example:
            >>> job_mgr = JobManagement()
            >>> info_mgmt_settings = job_mgr.get_priority_setting("Information Management")
            >>> print(info_mgmt_settings)
            {'jobTypeName': 'Information Management', 'combinedPriority': 0, 'type_of_operation': 1}

            >>> windows_fs_settings = job_mgr.get_priority_setting("Windows File System")
            >>> print(windows_fs_settings)
            {'appTypeName': 'Windows File System', 'combinedPriority': 6, 'type_of_operation': 2}

        #ai-gen-doc
        """
        if isinstance(jobtype, str):
            for job_type in self._priority_settings['jobPrioritySettings']['jobTypePriorityList']:
                if job_type['jobTypeName'] == jobtype:
                    settings = {
                        'jobTypeName': job_type.get('jobTypeName'),
                        'combinedPriority': job_type.get('combinedPriority'),
                        'type_of_operation': 1
                    }
                    return settings
            for job_type in self._priority_settings['jobPrioritySettings']['agentTypePriorityList']:
                if job_type['agentTypeEntity']['appTypeName'] == jobtype:
                    settings = {
                        'appTypeName': job_type.get('agentTypeEntity').get('appTypeName'),
                        'combinedPriority': job_type.get('combinedPriority'),
                        'type_of_operation': 2
                    }
                    return settings
        else:
            raise SDKException('Job', '108')

    def get_update_setting(self, jobtype: str) -> Dict[str, Any]:
        """Retrieve update settings associated with a specific job type.

        Args:
            jobtype: The name of the job type for which to obtain update settings (e.g., "Windows File System").
                For available job types, refer to the documentation of the `get_priority_setting(jobtype)` method.

        Returns:
            Dictionary containing the update settings for the specified job type, such as:
                {
                    "appTypeName": "Windows File System",
                    "recoveryTimeInMinutes": 20,
                    "protectionTimeInMinutes": 20
                }

        Raises:
            SDKException: If the input jobtype is not a valid string.

        Example:
            >>> job_mgr = JobManagement()
            >>> settings = job_mgr.get_update_setting("Windows File System")
            >>> print(settings)
            {'appTypeName': 'Windows File System', 'recoveryTimeInMinutes': 20, 'protectionTimeInMinutes': 20}
        #ai-gen-doc
        """
        if isinstance(jobtype, str):
            for job_type in self._update_settings['jobUpdatesSettings']['agentTypeJobUpdateIntervalList']:
                if job_type['agentTypeEntity']['appTypeName'] == jobtype:
                    settings = {
                        'appTypeName': job_type.get('agentTypeEntity').get('appTypeName'),
                        'recoveryTimeInMinutes': job_type.get('recoveryTimeInMinutes'),
                        'protectionTimeInMinutes': job_type.get('protectionTimeInMinutes')
                    }
                    return settings
        else:
            raise SDKException('Job', '108')

    @property
    def general_settings(self) -> Dict[str, Any]:
        """Get the general settings for job management.

        Returns:
            Dictionary containing the general settings configuration.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> settings = job_mgmt.general_settings  # Use dot notation for property access
            >>> print("General settings:", settings)
            >>> # The returned dictionary contains key-value pairs for job management settings

        #ai-gen-doc
        """
        return self._general_settings

    @property
    def restart_settings(self) -> Dict[str, Any]:
        """Get the restart settings for the job management.

        Returns:
            Dictionary containing the restart settings for jobs.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> settings = job_mgmt.restart_settings  # Use dot notation for property access
            >>> print(f"Restart settings: {settings}")
            >>> # The returned dictionary contains configuration for job restarts

        #ai-gen-doc
        """

        return self._restart_settings

    @property
    def priority_settings(self) -> Dict[str, Any]:
        """Get the priority settings for job management.

        Returns:
            Dictionary containing the current priority settings.

        Example:
            >>> job_mgmt = JobManagement(...)
            >>> settings = job_mgmt.priority_settings  # Use dot notation for property access
            >>> print(f"Priority settings: {settings}")
            >>> # The returned dictionary contains priority configuration details

        #ai-gen-doc
        """

        return self._priority_settings

    @property
    def update_settings(self) -> Dict[str, Any]:
        """Get the update settings for the job management system.

        Returns:
            Dictionary containing the current update settings.

        Example:
            >>> job_mgmt = JobManagement()
            >>> settings = job_mgmt.update_settings  # Use dot notation for property access
            >>> print(f"Update settings: {settings}")
            >>> # The returned dictionary contains configuration details for updates

        #ai-gen-doc
        """

        return self._update_settings

    def set_job_error_threshold(self, error_threshold_dict: Dict[str, Any]) -> None:
        """Set the error threshold parameters for job management.

        Args:
            error_threshold_dict: Dictionary containing key/value pairs for error threshold settings.
                Example keys may include 'max_errors', 'error_percentage', or other job-specific thresholds.

        Example:
            >>> job_mgr = JobManagement()
            >>> error_thresholds = {
            ...     'max_errors': 5,
            ...     'error_percentage': 10
            ... }
            >>> job_mgr.set_job_error_threshold(error_thresholds)
            >>> # The error thresholds for job management are now set

        #ai-gen-doc
        """
        raise NotImplementedError("Yet To Be Implemented")


class Job(object):
    """
    Represents a job for performing client operations within a CommCell environment.

    This class provides comprehensive management and monitoring capabilities for jobs
    associated with a specific client. It allows users to access detailed job properties,
    control job execution (pause, resume, kill, resubmit), retrieve job summaries and details,
    and interact with job-related logs and events.

    Key Features:
        - Initialization and validation of job instances
        - Access to extensive job properties (status, type, timing, client/agent info, etc.)
        - Job control operations: pause, resume, kill, resubmit
        - Wait for job status changes and completion with timeout support
        - Retrieval of job summaries, details, and advanced information
        - Access to job events, logs, VM lists, and child jobs
        - Ability to send job logs via email
        - Refresh and update job information
        - Task-level details and statistics (objects, files transferred, media size, etc.)

    This class is intended for use in environments where detailed job management and
    monitoring are required for client operations, providing a rich interface for
    interacting with job lifecycle and metadata.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', job_id: Union[str, int]) -> None:
        """Initialize a Job instance for managing backup or restore jobs.

        Args:
            commcell_object: Instance of the Commcell class representing the Commcell connection.
            job_id: The job ID as a string or integer.

        Raises:
            SDKException: If the job ID is not an integer or if the job does not exist in the Commcell.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> job = Job(commcell, 12345)
            >>> print(f"Job initialized with ID: {job.job_id}")
            >>> # The Job object can now be used to query job details and perform job operations

        #ai-gen-doc
        """
        try:
            int(job_id)
        except ValueError:
            raise SDKException('Job', '101')

        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._job_id = str(job_id)

        self._JOB = self._services['JOB'] % (self.job_id)

        if not self._is_valid_job():
            raise SDKException('Job', '102', f'No job exists with the specified Job ID: {self.job_id}')

        self._JOB_DETAILS = self._services['JOB_DETAILS']
        self.ADVANCED_JOB_DETAILS = AdvancedJobDetailType
        self._SUSPEND = self._services['SUSPEND_JOB'] % self.job_id
        self._RESUME = self._services['RESUME_JOB'] % self.job_id
        self._KILL = self._services['KILL_JOB'] % self.job_id
        self._RESUBMIT = self._services['RESUBMIT_JOB'] % self.job_id
        self._JOB_EVENTS = self._services['JOB_EVENTS'] % self.job_id
        self._JOB_TASK_DETAILS = self._services['JOB_TASK_DETAILS']

        self._client_name = None
        self._agent_name = None
        self._instance_name = None
        self._backupset_name = None
        self._subclient_name = None
        self._job_type = None
        self._backup_level = None
        self._start_time = None
        self._end_time = None
        self._delay_reason = None
        self._pending_reason = None
        self._status = None
        self._phase = None
        self._summary = None
        self._details = None
        self._task_details = None

        self.refresh()

    def __repr__(self) -> str:
        """Return a string representation of the Job instance.

        This method provides a human-readable description of the Job object, 
        including its job ID. Useful for debugging and logging purposes.

        Returns:
            str: String representation of the Job instance.

        Example:
            >>> job = Job(...)
            >>> print(repr(job))
            Job class instance for job id: "12345"
        #ai-gen-doc
        """
        representation_string = 'Job class instance for job id: "{0}"'
        return representation_string.format(self.job_id)

    def _is_valid_job(self) -> bool:
        """Check if the job associated with the current job ID is valid.

        This method attempts to retrieve the job summary up to 10 times, handling transient errors
        specific to job validation. If the job summary is successfully retrieved, the job is considered valid.

        Returns:
            True if the job is valid, False otherwise.

        Example:
            >>> job = Job(...)
            >>> is_valid = job._is_valid_job()
            >>> print(f"Is job valid? {is_valid}")

        #ai-gen-doc
        """
        for _ in range(10):
            try:
                self._get_job_summary()
                return True
            except SDKException as excp:
                if excp.exception_module == 'Job' and excp.exception_id == '104':
                    time.sleep(1.5)
                    continue
                else:
                    raise excp

        return False

    def _get_job_summary(self) -> Dict[str, Any]:
        """Retrieve the summary properties of this job.

        This method attempts to fetch the job summary details from the Commcell server,
        retrying up to five times to handle transient cases where job records may not be immediately available.

        Returns:
            Dictionary containing the summary information for the job.

        Raises:
            SDKException: If no record is found for this job, if the response is empty,
                or if the response indicates a failure.

        Example:
            >>> job = Job(...)
            >>> summary = job._get_job_summary()
            >>> print(f"Job Summary: {summary}")
            >>> # The returned dictionary contains key details about the job

        #ai-gen-doc
        """
        attempts = 0
        while attempts < 5:  # Retrying to ignore the transient case when no jobs are found
            flag, response = self._cvpysdk_object.make_request('GET', self._JOB)
            attempts += 1

            if flag:
                if response.json():
                    if response.json().get('totalRecordsWithoutPaging', 0) == 0:
                        time.sleep(2**attempts)
                        continue

                    if 'jobs' in response.json():
                        for job in response.json()['jobs']:
                            return job['jobSummary']
                else:
                    if attempts > 4:
                        raise SDKException('Response', '102')
                    time.sleep(20)

            else:
                if attempts > 4:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
                time.sleep(20)

        raise SDKException('Job', '104')

    def _get_job_details(self) -> Dict[str, Any]:
        """Retrieve the detailed properties of this job.

        This method fetches comprehensive information about the job, including its status,
        attempts, and any associated error details. It performs multiple retries to handle
        transient cases where job details may not be immediately available.

        Returns:
            Dictionary containing the detailed properties of the job.

        Raises:
            SDKException: If the job details cannot be retrieved, the response is empty,
                or the response indicates a failure.

        Example:
            >>> job = Job(...)
            >>> details = job._get_job_details()
            >>> print(details)
            >>> # The returned dictionary contains job properties such as status, attempts, etc.

        #ai-gen-doc
        """
        payload = {
            "jobId": int(self.job_id),
            "showAttempt": True
        }

        retry_count = 0

        while retry_count < 5:  # Retrying to ignore the transient case when job details are not found
            flag, response = self._cvpysdk_object.make_request('POST', self._JOB_DETAILS, payload)
            retry_count += 1

            if flag:
                if response.json():
                    if 'job' in response.json():
                        return response.json()['job']
                    elif 'error' in response.json():
                        error_code = response.json()['error']['errList'][0]['errorCode']
                        error_message = response.json()['error']['errList'][0]['errLogMessage']

                        raise SDKException(
                            'Job',
                            '105',
                            'Error Code: "{0}"\nError Message: "{1}"'.format(error_code, error_message)
                        )
                    else:
                        raise SDKException('Job', '106', 'Response JSON: {0}'.format(response.json()))
                else:
                    if retry_count > 4:
                        raise SDKException('Response', '102')
                    time.sleep(20)
            else:
                if retry_count > 4:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
                time.sleep(20)

        raise SDKException('Response', '102')

    def _get_job_task_details(self) -> Dict[str, Any]:
        """Retrieve the task details associated with this job.

        This method attempts to fetch the job's task information from the Commcell server,
        retrying up to five times to handle transient issues. If successful, it returns a
        dictionary containing the task details. If the request fails, the response is empty,
        or the response indicates an error, an SDKException is raised.

        Returns:
            Dictionary containing the task details for the job.

        Raises:
            SDKException: If the job task details cannot be retrieved, the response is empty,
                or the response indicates an error.

        Example:
            >>> job = Job(...)
            >>> task_details = job._get_job_task_details()
            >>> print(f"Task details: {task_details}")
            >>> # The returned dictionary contains information about the job's associated task

        #ai-gen-doc
        """
        retry_count = 0

        while retry_count < 5:  # Retrying to ignore the transient case when job task details are not found
            flag, response = self._cvpysdk_object.make_request('GET', self._JOB_TASK_DETAILS % self.job_id)
            retry_count += 1

            if flag:
                if response.json():
                    if 'taskInfo' in response.json():
                        return response.json()['taskInfo']
                    elif 'error' in response.json():
                        error_code = response.json()['error']['errList'][0]['errorCode']
                        error_message = response.json()['error']['errList'][0]['errorMessage']

                        raise SDKException(
                            'Job',
                            '105',
                            'Error Code: "{0}"\nError Message: "{1}"'.format(error_code, error_message)
                        )
                    else:
                        raise SDKException('Job', '106', 'Response JSON: {0}'.format(response.json()))
                else:
                    if retry_count > 4:
                        raise SDKException('Response', '102')
                    time.sleep(20)
            else:
                if retry_count > 4:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
                time.sleep(20)

        raise SDKException('Response', '102')

    def _initialize_job_properties(self) -> None:
        """Initialize common properties for the job object.

        This method sets up essential job attributes such as client, agent, backupset, 
        and subclient names, along with job status and start time. It retrieves job 
        summary and details, and formats the job start time for easy access.

        Example:
            >>> job = Job(...)
            >>> job._initialize_job_properties()
            >>> print(f"Job status: {job._status}")
            >>> print(f"Job started at: {job._start_time}")
            >>> # The job object now contains updated summary and details information

        #ai-gen-doc
        """
        self._summary = self._get_job_summary()
        self._details = self._get_job_details()

        self._status = self._summary['status']

        self._start_time = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.gmtime(self._summary['jobStartTime'])
        )

    def _wait_for_status(self, status: str, timeout: int = 6) -> None:
        """Wait for the job status to change to the specified value or until the timeout is reached.

        This method monitors the job status and waits until it matches the provided status string,
        or until the specified timeout interval (in minutes) has elapsed, whichever occurs first.

        Args:
            status: The target job status to wait for (case-insensitive).
            timeout: Maximum time to wait in minutes before giving up. Defaults to 6 minutes.

        Example:
            >>> job = Job(...)
            >>> job._wait_for_status('Completed', timeout=10)
            >>> # The method will return when the job status is 'Completed' or after 10 minutes

        #ai-gen-doc
        """
        start_time = time.time()
        current_job_status = self.status
        current_job_status = current_job_status if current_job_status else self.state
        while current_job_status.lower() != status.lower():
            if (self.is_finished is True) or (time.time() - start_time > (timeout * 60)):
                break

            time.sleep(3)
            current_job_status = self.status

    def wait_for_completion(self, timeout: int = 30, **kwargs: Any) -> bool:
        """Wait until the job completes or exceeds the specified timeout.

        This method monitors the job's status and waits until it is finished. If the job remains in 
        'Pending' or 'Waiting' state for longer than the specified timeout (in minutes), the job is 
        killed and logs are sent to configured email addresses. Optionally, you can specify 
        'return_timeout' in kwargs to force the method to return False after a given number of minutes.

        In case of job failure, you can obtain the job status and failure reason using the 
        `status` and `delay_reason` properties.

        Args:
            timeout: Number of minutes to wait before killing the job if it remains in 'Pending' or 
                'Waiting' state. Default is 30.
            **kwargs: Optional arguments.
                return_timeout (int): Number of minutes after which the method will return False 
                    regardless of job status.

        Returns:
            True if the job finished successfully.
            False if the job was killed, failed, or timed out.

        Example:
            >>> job = Job(...)
            >>> success = job.wait_for_completion(timeout=45, return_timeout=60)
            >>> print(f"Job completed: {success}")
            >>> # If False, check job.status and job.delay_reason for details

        #ai-gen-doc
        """
        start_time = actual_start_time = time.time()
        pending_time = 0
        waiting_time = 0
        previous_status = None
        return_timeout = kwargs.get('return_timeout')
        email_ids = self._commcell_object.job_logs_emails
        status_list = ['pending', 'waiting']

        while not self.is_finished:
            time.sleep(30)

            if return_timeout and ((time.time() - actual_start_time) / 60) > return_timeout:
                return False

            # get the current status of the job
            status = self.status
            status = status.lower() if status else self.state.lower()

            # set the value of start time as current time
            # if the current status is pending / waiting but the previous status was not
            # also if the current status is pending / waiting and same as previous,
            # then don't update the value of start time
            if status in status_list and previous_status not in status_list:
                start_time = time.time()

            if status == 'pending':
                pending_time = (time.time() - start_time) / 60
            else:
                pending_time = 0

            if status == 'waiting':
                waiting_time = (time.time() - start_time) / 60
            else:
                waiting_time = 0

            if pending_time > timeout or waiting_time > timeout:
                self.kill()
                if len(email_ids):
                    self.send_logs(email_ids=email_ids)
                break

            # set the value of previous status as the value of current status
            previous_status = status
        else:
            if self._status.lower() not in ["failed", "killed", "failed to start"]:
               return True
            else:
                if len(email_ids):
                    self.send_logs(email_ids=email_ids)
                return False
        return False

    @property
    def is_finished(self) -> bool:
        """Check whether the job has finished.

        This property evaluates the job's status to determine if it has reached a terminal state,
        such as completed, killed, committed, or failed.

        Returns:
            True if the job has finished (completed, killed, committed, or failed), False otherwise.

        Example:
            >>> job = Job(...)
            >>> if job.is_finished:
            ...     print("Job has finished.")
            ... else:
            ...     print("Job is still running.")

        #ai-gen-doc
        """
        self._summary = self._get_job_summary()
        self._details = self._get_job_details()

        self._status = self._summary['status']

        if self._summary['lastUpdateTime'] != 0:
            self._end_time = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.gmtime(self._summary['lastUpdateTime'])
            )

        return ('completed' in self._status.lower() or
                'killed' in self._status.lower() or
                'committed' in self._status.lower() or
                'failed' in self._status.lower())

    @property
    def client_name(self) -> str:
        """Get the name of the client associated with this job as a read-only property.

        Returns:
            The client name as a string.

        Example:
            >>> job = Job(...)
            >>> client = job.client_name  # Use dot notation for property access
            >>> print(f"Client name: {client}")
            >>> # The returned value is the name of the client for this job

        #ai-gen-doc
        """
        if 'clientName' in self._summary['subclient']:
            return self._summary['subclient']['clientName']

    @property
    def agent_name(self) -> Optional[str]:
        """Get the agent name associated with this job as a read-only property.

        Returns:
            The agent name as a string if available, otherwise None.

        Example:
            >>> job = Job(...)
            >>> agent = job.agent_name  # Use dot notation for property access
            >>> print(f"Agent name: {agent}")
            >>> # The agent name is read-only and cannot be modified directly

        #ai-gen-doc
        """
        if 'appName' in self._summary['subclient']:
            return self._summary['subclient']['appName']

    @property
    def instance_name(self) -> str:
        """Get the instance name associated with this job as a read-only property.

        Returns:
            The instance name as a string.

        Example:
            >>> job = Job(...)
            >>> name = job.instance_name  # Use dot notation for property access
            >>> print(f"Instance name: {name}")

        #ai-gen-doc
        """
        if 'instanceName' in self._summary['subclient']:
            return self._summary['subclient']['instanceName']

    @property
    def backupset_name(self) -> str:
        """Get the name of the backupset associated with this job as a read-only property.

        Returns:
            The backupset name as a string.

        Example:
            >>> job = Job(...)
            >>> name = job.backupset_name  # Use dot notation for property access
            >>> print(f"Backupset name: {name}")
            >>> # The returned string represents the backupset name for this job

        #ai-gen-doc
        """
        if 'backupsetName' in self._summary['subclient']:
            return self._summary['subclient']['backupsetName']

    @property
    def subclient_name(self) -> str:
        """Get the name of the subclient associated with this job as a read-only property.

        Returns:
            The subclient name as a string.

        Example:
            >>> job = Job(...)
            >>> name = job.subclient_name  # Use dot notation for property access
            >>> print(f"Subclient name: {name}")
        #ai-gen-doc
        """
        if 'subclientName' in self._summary['subclient']:
            return self._summary['subclient']['subclientName']

    @property
    def status(self) -> str:
        """Get the current status of the job as a read-only property.

        The job status indicates the current state of the job, such as 'Running', 'Completed', 'Failed', etc.
        For a complete list of possible status values, refer to the official documentation:
        http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm

        Returns:
            The status of the job as a string.

        Example:
            >>> job = Job(...)
            >>> current_status = job.status  # Use dot notation to access the property
            >>> print(f"Job status: {current_status}")
            >>> # Possible status values include 'Running', 'Completed', 'Failed', etc.

        #ai-gen-doc
        """
        self.is_finished
        return self._status

    @property
    def job_id(self) -> int:
        """Get the unique identifier for this job as a read-only property.

        Returns:
            The job ID as an integer.

        Example:
            >>> job = Job(...)
            >>> print(f"Job ID: {job.job_id}")  # Access job_id using dot notation
            >>> # The job_id property provides the unique identifier for the job

        #ai-gen-doc
        """
        return self._job_id

    @property
    def job_type(self) -> str:
        """Get the type of the job as a read-only property.

        Returns:
            The job type as a string (e.g., 'Backup', 'Restore', etc.).

        Example:
            >>> job = Job(...)
            >>> print(job.job_type)  # Use dot notation for property access
            >>> # Output might be: 'Backup'
        #ai-gen-doc
        """
        return self._summary['jobType']

    @property
    def backup_level(self) -> str:
        """Get the backup level name for this job as a read-only property.

        Returns:
            The backup level name as a string (e.g., 'Full', 'Incremental', 'Differential').

        Example:
            >>> job = Job(...)
            >>> level = job.backup_level  # Use dot notation for property access
            >>> print(f"Backup level: {level}")
            >>> # The returned value indicates the type of backup performed for the job

        #ai-gen-doc
        """
        if 'backupLevelName' in self._summary:
            return self._summary['backupLevelName']

    @property
    def start_time(self) -> str:
        """Get the start time of the job as a read-only property.

        Returns:
            The start time of the job as a string, typically in ISO 8601 format.

        Example:
            >>> job = Job(...)
            >>> print(f"Job started at: {job.start_time}")
            >>> # The start_time property provides the timestamp when the job began

        #ai-gen-doc
        """
        return self._start_time
    
    @property
    def start_timestamp(self) -> int:
        """Get the Unix start time of the job as a read-only property.

        Returns:
            The job's start time as a Unix timestamp (integer).

        Example:
            >>> job = Job(...)
            >>> start_time = job.start_timestamp  # Use dot notation for property access
            >>> print(f"Job started at Unix time: {start_time}")
        #ai-gen-doc
        """
        return self._summary['jobStartTime']

    @property
    def end_timestamp(self) -> int:
        """Get the Unix end timestamp of the job as a read-only property.

        Returns:
            The job's end time as a Unix timestamp (integer).

        Example:
            >>> job = Job(...)
            >>> end_time = job.end_timestamp  # Use dot notation for property access
            >>> print(f"Job ended at Unix time: {end_time}")

        #ai-gen-doc
        """
        return self._summary['jobEndTime']

    @property
    def end_time(self) -> str:
        """Get the end time of the job as a read-only property.

        Returns:
            The end time of the job as a string, typically in a standard datetime format.

        Example:
            >>> job = Job(...)
            >>> print(f"Job ended at: {job.end_time}")
            >>> # The end_time property provides the completion time of the job

        #ai-gen-doc
        """
        return self._end_time

    @property
    def delay_reason(self) -> Optional[str]:
        """Get the reason for the job delay as a read-only property.

        Returns:
            The delay reason as a string if available, otherwise None.

        Example:
            >>> job = Job(...)
            >>> reason = job.delay_reason  # Use dot notation for property access
            >>> if reason:
            >>>     print(f"Job delay reason: {reason}")
            >>> else:
            >>>     print("No delay reason found for this job.")

        #ai-gen-doc
        """
        self.is_finished
        progress_info = self._details['jobDetail']['progressInfo']
        if 'reasonForJobDelay' in progress_info and progress_info['reasonForJobDelay']:
            return progress_info['reasonForJobDelay']

    @property
    def pending_reason(self) -> Optional[str]:
        """Get the pending reason for the job as a read-only property.

        Returns:
            The pending reason for the job as a string, or None if not available.

        Example:
            >>> job = Job(...)
            >>> reason = job.pending_reason  # Use dot notation for property access
            >>> if reason:
            >>>     print(f"Job is pending due to: {reason}")
            >>> else:
            >>>     print("No pending reason for this job.")
        #ai-gen-doc
        """
        self.is_finished
        if 'pendingReason' in self._summary and self._summary['pendingReason']:
            return self._summary['pendingReason']

    @property
    def phase(self) -> str:
        """Get the current phase name of the job as a read-only property.

        Returns:
            The name of the current phase of the job as a string.

        Example:
            >>> job = Job(...)
            >>> current_phase = job.phase  # Use dot notation for property access
            >>> print(f"Job is currently in phase: {current_phase}")

        #ai-gen-doc
        """
        self.is_finished
        if 'currentPhaseName' in self._summary:
            return self._summary['currentPhaseName']

    @property
    def attempts(self) -> Dict[str, Any]:
        """Get the job attempts data as a read-only property.

        Returns:
            Dictionary containing information about each attempt made for the job.
            The structure typically includes details such as attempt number, status, and timestamps.

        Example:
            >>> job = Job(...)
            >>> attempts_info = job.attempts  # Use dot notation for property access
            >>> print(f"Job attempts: {attempts_info}")
            >>> # You can inspect individual attempt details from the returned dictionary

        #ai-gen-doc
        """
        self.is_finished
        return self._details.get('jobDetail', {}).get('attemptsInfo', {})

    @property
    def summary(self) -> Dict[str, Any]:
        """Get the full summary of the job as a read-only property.

        Returns:
            Dictionary containing detailed information about the job summary.

        Example:
            >>> job = Job(...)
            >>> job_summary = job.summary  # Access summary using dot notation
            >>> print(job_summary)
            >>> # The summary dictionary includes job status, details, and other metadata

        #ai-gen-doc
        """
        self.is_finished
        return self._summary

    @property
    def username(self) -> str:
        """Get the username associated with this job as a read-only property.

        Returns:
            The username as a string.

        Example:
            >>> job = Job(...)
            >>> user = job.username  # Access the username property
            >>> print(f"Job executed by user: {user}")
        #ai-gen-doc
        """
        return self._summary['userName']['userName']

    @property
    def userid(self) -> str:
        """Get the user ID associated with this job as a read-only property.

        Returns:
            The user ID as a string.

        Example:
            >>> job = Job(...)
            >>> user_id = job.userid  # Access the user ID property
            >>> print(f"Job submitted by user ID: {user_id}")
        #ai-gen-doc
        """
        return self._summary['userName']['userId']

    @property
    def details(self) -> Dict[str, Any]:
        """Get the full details of the job as a read-only property.

        Returns:
            Dictionary containing all available information about the job.

        Example:
            >>> job = Job(...)
            >>> job_info = job.details  # Use dot notation for properties
            >>> print(f"Job details: {job_info}")
            >>> # Access specific job attributes from the returned dictionary

        #ai-gen-doc
        """
        self.is_finished
        return self._details

    @property
    def size_of_application(self) -> int:
        """Get the size of the application associated with this job.

        This property provides the total size of the application processed by the job,
        typically measured in bytes. It is a read-only attribute and reflects the value
        stored in the job summary.

        Returns:
            The size of the application as an integer (in bytes).

        Example:
            >>> job = Job(...)
            >>> app_size = job.size_of_application  # Use dot notation for properties
            >>> print(f"Application size: {app_size} bytes")
        #ai-gen-doc
        """
        if 'sizeOfApplication' in self._summary:
            return self._summary['sizeOfApplication']

    @property
    def media_size(self) -> int:
        """Get the size of media or data written for this job.

        This property provides the total size of media on disk associated with the job,
        as reported in the job summary.

        Returns:
            The size of media on disk in bytes as an integer.

        Example:
            >>> job = Job(...)
            >>> size = job.media_size  # Use dot notation for property access
            >>> print(f"Media size: {size} bytes")
        #ai-gen-doc
        """
        return self._summary.get('sizeOfMediaOnDisk', 0)

    @property
    def job_end_time(self) -> int:
        """Get the end time of the backup job as a read-only property.

        Returns:
            The job's end time as a Unix timestamp (integer). If the end time is unavailable, returns -1.

        Example:
            >>> job = Job(...)
            >>> end_time = job.job_end_time  # Use dot notation for property access
            >>> print(f"Job ended at Unix timestamp: {end_time}")
            >>> # You can convert the Unix timestamp to a human-readable format if needed

        #ai-gen-doc
        """
        return self._details.get('jobDetail', {}).get('detailInfo',{}).get('endTime',-1)

    @property
    def num_of_objects(self) -> int:
        """Get the number of objects backed up by this job as a read-only property.

        Returns:
            The number of objects backed up in the job as an integer. If the information is unavailable, returns -1.

        Example:
            >>> job = Job(...)
            >>> num_objects = job.num_of_objects  # Use dot notation for property access
            >>> print(f"Number of objects backed up: {num_objects}")

        #ai-gen-doc
        """
        return self._details.get('jobDetail', {}).get('detailInfo', {}).get('numOfObjects', -1)

    @property
    def num_of_files_transferred(self) -> int:
        """Get the number of files transferred for this job.

        This property provides the count of files that have been successfully transferred 
        during the execution of the job. It is read-only and automatically updated as the job progresses.

        Returns:
            The number of files transferred as an integer.

        Example:
            >>> job = Job(...)
            >>> files_transferred = job.num_of_files_transferred  # Use dot notation for properties
            >>> print(f"Files transferred: {files_transferred}")

        #ai-gen-doc
        """
        self.is_finished
        return self._details['jobDetail']['progressInfo']['numOfFilesTransferred']

    @property
    def state(self) -> str:
        """Get the current state of the job as a read-only property.

        Returns:
            The job state as a string, indicating the current progress or status.

        Example:
            >>> job = Job(...)
            >>> current_state = job.state  # Use dot notation for property access
            >>> print(f"Job state: {current_state}")
            >>> # Possible states include 'Running', 'Completed', 'Failed', etc.

        #ai-gen-doc
        """
        self.is_finished
        return self._details['jobDetail']['progressInfo']['state']

    @property
    def task_details(self) -> Dict[str, Any]:
        """Get the dictionary containing detailed information about the job's tasks.

        Returns:
            Dictionary with job task details, such as task IDs, status, and related metadata.

        Example:
            >>> job = Job(...)
            >>> details = job.task_details  # Use dot notation for property access
            >>> print(details)
            >>> # Access specific task information
            >>> if 'task_id' in details:
            >>>     print(f"Task ID: {details['task_id']}")

        #ai-gen-doc
        """
        if not self._task_details:
            self._task_details = self._get_job_task_details()
        return self._task_details

    def pause(self, wait_for_job_to_pause: bool = False, timeout: int = 6) -> None:
        """Suspend the current job and optionally wait until it is paused.

        This method sends a request to suspend the job. If `wait_for_job_to_pause` is True,
        it will wait until the job status changes to "SUSPENDED" or until the specified timeout elapses.

        Args:
            wait_for_job_to_pause: Whether to wait until the job status is changed to "SUSPENDED".
                Defaults to False.
            timeout: Maximum time in seconds to wait for the job to move to the suspended state.
                Defaults to 6.

        Raises:
            SDKException: If the job fails to suspend or if the response is not successful.

        Example:
            >>> job = Job(...)
            >>> job.pause(wait_for_job_to_pause=True, timeout=10)
            >>> print("Job has been suspended.")
        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._SUSPEND)

        self.is_finished

        if flag:
            if response.json():
                if 'errors' in response.json():
                    error_list = response.json()['errors'][0]['errList'][0]
                    error_code = error_list['errorCode']
                    error_message = error_list['errLogMessage'].strip()
                else:
                    error_code = response.json().get('errorCode', 0)
                    error_message = response.json().get('errorMessage', 'nil')

                if error_code != 0:
                    raise SDKException(
                        'Job', '102', 'Job suspend failed\nError: "{0}"'.format(error_message)
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if wait_for_job_to_pause is True:
            self._wait_for_status("SUSPENDED", timeout=timeout)

    def resume(self, wait_for_job_to_resume: bool = False) -> None:
        """Resume the job, optionally waiting until the job status changes to 'Running'.

        Args:
            wait_for_job_to_resume: If True, the method waits until the job status is updated to 'Running'.
                Defaults to False.

        Raises:
            SDKException: If the job fails to resume or if the response from the server is not successful.

        Example:
            >>> job = Job(...)
            >>> job.resume()  # Resume the job without waiting for status change
            >>> 
            >>> # Resume the job and wait until it is running
            >>> job.resume(wait_for_job_to_resume=True)

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._RESUME)

        self.is_finished

        if flag:
            if response.json():
                if 'errors' in response.json():
                    error_list = response.json()['errors'][0]['errList'][0]
                    error_code = error_list['errorCode']
                    error_message = error_list['errLogMessage'].strip()
                else:
                    error_code = response.json().get('errorCode', 0)
                    error_message = response.json().get('errorMessage', 'nil')

                if error_code != 0:
                    raise SDKException(
                        'Job', '102', 'Job resume failed\nError: "{0}"'.format(error_message)
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if wait_for_job_to_resume is True:
            self._wait_for_status("RUNNING")

    def resubmit(self, start_suspended: Optional[bool] = None) -> 'Job':
        """Resubmit the current job, optionally starting the new job in a suspended state.

        Args:
            start_suspended: Whether to start the resubmitted job in a suspended state.
                - True: Start the new job suspended.
                - False: Start the new job active.
                - None (default): Start the new job in the same state as the original job.

        Returns:
            Job: A new Job object representing the resubmitted job.

        Raises:
            SDKException: If the job is still running or if the resubmission fails.

        Example:
            >>> job = Job(commcell_object, job_id)
            >>> new_job = job.resubmit(start_suspended=True)
            >>> print(f"Resubmitted job ID: {new_job.job_id}")
            >>> # The returned Job object can be used to monitor or manage the new job

        #ai-gen-doc
        """
        if start_suspended not in [True, False, None]:
            raise SDKException('Job', '108')

        if not self.is_finished:
            raise SDKException('Job', '102', 'Cannot resubmit the Job, the Job is still running')

        url = self._RESUBMIT
        if start_suspended is not None:
            url += f'?startInSuspendedState={start_suspended}'
        flag, response = self._cvpysdk_object.make_request('POST', url)

        if flag:
            if response.json():
                if 'errors' in response.json():
                    error_list = response.json()['errors'][0]['errList'][0]
                    error_code = error_list['errorCode']
                    error_message = error_list['errLogMessage'].strip()
                else:
                    error_code = response.json().get('errorCode', 0)
                    error_message = response.json().get('errorMessage', 'nil')

                if error_code != 0:
                    raise SDKException(
                        'Job', '102', 'Resubmitting job failed\nError: "{0}"'.format(error_message)
                    )
            return Job(self._commcell_object, response.json()['jobIds'][0])
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def kill(self, wait_for_job_to_kill: bool = False) -> None:
        """Terminate the current job and optionally wait until its status is 'Killed'.

        Args:
            wait_for_job_to_kill: If True, waits until the job status changes to 'Killed'.
                Defaults to False.

        Raises:
            SDKException: If the job fails to terminate or the response indicates an error.

        Example:
            >>> job = Job(...)
            >>> job.kill()  # Terminates the job without waiting for status change
            >>> 
            >>> # To wait until the job status is 'Killed'
            >>> job.kill(wait_for_job_to_kill=True)

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._KILL)

        self.is_finished

        if flag:
            if response.json():
                if 'errors' in response.json():
                    error_list = response.json()['errors'][0]['errList'][0]
                    error_code = error_list['errorCode']
                    error_message = error_list['errLogMessage'].strip()
                else:
                    error_code = response.json().get('errorCode', 0)
                    error_message = response.json().get('errorMessage', 'nil')

                if error_code != 0:
                    raise SDKException(
                        'Job', '102', 'Job kill failed\nError: "{0}"'.format(error_message)
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if wait_for_job_to_kill is True:
            self._wait_for_status("KILLED")

    def send_logs(self, email_ids: Optional[List[str]] = None) -> bool:
        """Send the logs of the current job to specified email addresses.

        This method sends the job logs to the provided list of email addresses. If no email addresses are specified,
        the logs will not be sent to any recipients. The method waits for the log sending task to complete and
        returns True if successful. If the operation fails, an SDKException is raised.

        Args:
            email_ids: Optional list of email addresses to which the job logs should be sent. If None, no emails are sent.

        Returns:
            True if the logs were sent successfully.

        Raises:
            SDKException: If the log sending operation fails or the response contains an error.

        Example:
            >>> job = Job(commcell_object, job_id)
            >>> success = job.send_logs(['admin@example.com', 'support@example.com'])
            >>> print(f"Logs sent successfully: {success}")
            >>> # If no email addresses are provided, logs will not be sent to any recipients
            >>> job.send_logs()
        #ai-gen-doc
        """
        if email_ids is None:
            email_ids = []
        details = self._get_job_details()
        failure_reason = details.get('jobDetail', {}).get('clientStatusInfo', {}).get('vmStatus', [{}])[0].get(
            'FailureReason', '')
        request_json = {
            "taskInfo": {
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 1,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 5010
                        },
                        "options": {
                            "adminOpts": {
                                "sendLogFilesOption": {
                                    "actionLogsEndJobId": 0,
                                    "emailSelected": True,
                                    "jobid": int(self._job_id),
                                    "tsDatabase": False,
                                    "galaxyLogs": True,
                                    "getLatestUpdates": False,
                                    "actionLogsStartJobId": 0,
                                    "computersSelected": False,
                                    "csDatabase": False,
                                    "otherDatabases": False,
                                    "crashDump": False,
                                    "isNetworkPath": False,
                                    "saveToFolderSelected": False,
                                    "notifyMe": True,
                                    "includeJobResults": False,
                                    "doNotIncludeLogs": True,
                                    "machineInformation": False,
                                    "scrubLogFiles": False,
                                    "emailSubject": f"{self._commcell_object.commserv_name} : Logs for Job ID # {self._job_id} [Error]: {failure_reason}",
                                    "osLogs": False,
                                    "allUsersProfile": False,
                                    "splitFileSizeMB": 512,
                                    "actionLogs": False,
                                    "includeIndex": False,
                                    "databaseLogs": True,
                                    "includeDCDB": False,
                                    "collectHyperScale": False,
                                    "logFragments": False,
                                    "uploadLogsSelected": True,
                                    "useDefaultUploadOption": True,
                                    "enableChunking": True,
                                    "collectRFC": False,
                                    "collectUserAppLogs": False,
                                    "impersonateUser": {
                                        "useImpersonation": False
                                    },
                                    "clients": [
                                        {
                                            "clientId": 0,
                                            "clientName": None
                                        }
                                    ],
                                    "recipientTo": {
                                        "emailids": email_ids,
                                        "users": [],
                                        "userGroups": []
                                    },
                                    "sendLogsOnJobCompletion": False,
                                    "emailDescription": f"<h4>Error summary</h4> {failure_reason}"
                                }
                            }
                        }
                    }
                ]
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CREATE_TASK'], request_json
        )
        if flag:
            if response.json():
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    error_message = response.json().get('errorMessage', 'nil')
                    raise SDKException(
                        'Job', '102', 'Sending logs failed\nError: "{0}"'.format(error_message)
                    )
                else:
                    send_logs_job = Job(self._commcell_object, response.json()['jobIds'][0])
                    try:
                        send_logs_job.wait_for_completion()
                    except Exception as exp:
                        pass
                return True
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def refresh(self) -> None:
        """Reload the properties of the Job instance to reflect the latest state.

        This method updates the job's internal properties, ensuring that any changes 
        in the job's status or attributes are reflected in the object.

        Example:
            >>> job = Job(...)
            >>> job.refresh()  # Refresh job properties to get the latest status
            >>> print(f"Job finished: {job.is_finished}")
        #ai-gen-doc
        """
        self._initialize_job_properties()
        self.is_finished

    def advanced_job_details(self, info_type: 'AdvancedJobDetailType') -> Dict[str, Any]:
        """Retrieve advanced properties for the job based on the specified detail type.

        Args:
            info_type: An instance of AdvancedJobDetailType enum specifying the type of job details to retrieve.

        Returns:
            Dictionary containing advanced details for the specified job info type.

        Raises:
            SDKException: If the response is empty or unsuccessful.

        Example:
            >>> # Assuming job is an instance of Job and AdvancedJobDetailType is imported
            >>> details = job.advanced_job_details(AdvancedJobDetailType.SUMMARY)
            >>> print(details)
            >>> # The returned dictionary contains advanced job details for the requested type

        #ai-gen-doc
        """
        if not isinstance(info_type, AdvancedJobDetailType):
            raise SDKException('Response', '107')
        url = self._services['ADVANCED_JOB_DETAIL_TYPE'] % (self.job_id, info_type.value)
        flag, response = self._cvpysdk_object.make_request('GET', url)

        if flag:
            if response.json():
                response = response.json()

                if response.get('errorCode', 0) != 0:
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to fetch details.\nError: "{0}"'.format(error_message)
                    raise SDKException('Job', '102', o_str)

                return response
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_events(self) -> List[Dict[str, Any]]:
        """Retrieve the CommServe events associated with this job.

        Returns:
            List of dictionaries, each representing a job event with details such as severity, event code, job ID, subsystem, description, and client entity information.

        Example:
            >>> job = Job(...)
            >>> events = job.get_events()
            >>> print(f"Total events: {len(events)}")
            >>> if events:
            >>>     first_event = events[0]
            >>>     print(f"First event description: {first_event['description']}")
            >>>     print(f"Event severity: {first_event['severity']}")
            >>>     print(f"Client name: {first_event['clientEntity']['clientName']}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._JOB_EVENTS)
        if flag:
            if response.json() and 'commservEvents' in response.json():
                    return response.json()['commservEvents']
            raise SDKException('Job', '104')
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_vm_list(self) -> List[Dict[str, Any]]:
        """Retrieve the list of all virtual machines (VMs) associated with this job.

        Returns:
            List of dictionaries, each containing details about a VM associated with the job.
            Example VM dictionary fields include:
                - Size: int
                - AverageThroughput: int
                - UsedSpace: int
                - ArchivedByCurrentJob: bool
                - jobID: int
                - CBTStatus: str
                - BackupType: int
                - totalFiles: int
                - Status: int
                - CurrentThroughput: int
                - Agent: str
                - lastSyncedBkpJob: int
                - GUID: str
                - HardwareVersion: str
                - restoredSize: int
                - FailureReason: str
                - BackupStartTime: int
                - TransportMode: str
                - projectId: str
                - syncStatus: int
                - PoweredOffSince: int
                - OperatingSystem: str
                - backupLevel: int
                - destinationVMName: str
                - successfulCIedFiles: int
                - GuestSize: int
                - failedCIedFiles: int
                - vmName: str
                - ToolsVersion: str
                - clientId: int
                - Host: str
                - StubStatus: int
                - BackupEndTime: int
                - PoweredOffByCurrentJob: bool

        Example:
            >>> job = Job(...)
            >>> vm_list = job.get_vm_list()
            >>> print(f"Total VMs in job: {len(vm_list)}")
            >>> if vm_list:
            >>>     first_vm = vm_list[0]
            >>>     print(f"First VM name: {first_vm.get('vmName')}")
        #ai-gen-doc
        """
        return self.details.get('jobDetail', {}).get('clientStatusInfo', {}).get('vmStatus', [])

    def get_child_jobs(self) -> Optional[List[Dict[str, Any]]]:
        """Retrieve the child job details for the current job.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of dictionaries containing child job details if available,
            otherwise None.

        Example:
            >>> job = Job(...)
            >>> child_jobs = job.get_child_jobs()
            >>> if child_jobs:
            >>>     print(f"Found {len(child_jobs)} child jobs")
            >>>     for child in child_jobs:
            >>>         print(child)
            >>> else:
            >>>     print("No child jobs found for this job.")

        #ai-gen-doc
        """
        _jobs_list = []
        if self.details.get('jobDetail', {}).get('clientStatusInfo', {}).get('vmStatus'):
            for _job in self.details['jobDetail']['clientStatusInfo']['vmStatus']:
                _jobs_list.append(_job)
            return _jobs_list
        else:
            return None

    def get_logs(self) -> List[str]:
        """Retrieve the logs associated with the current job ID.

        Returns:
            List of log entries as strings, where each entry represents a line from the job logs.

        Raises:
            SDKException: If the logs cannot be retrieved or the response is invalid.

        Example:
            >>> job = Job(...)
            >>> logs = job.get_logs()
            >>> for line in logs:
            ...     print(line)
            >>> # Each line corresponds to a log entry for the job

        #ai-gen-doc
        """
        service = self._services['GET_LOGS'] % (self.job_id)
        flag, response = self._cvpysdk_object.make_request(method='GET', url=service)

        if flag:
            if response.text:
                return response.text.split('\n')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '102')


class _ErrorRule:
    """
    Manages error rules for application groups within a Commcell environment.

    This class provides functionality to add, enable, disable, retrieve, and delete error rules
    associated with specific application groups. It interacts with the underlying Commcell system
    to modify job statuses based on error conditions and supports XML-based rule definitions.

    Key Features:
        - Initialization with a Commcell instance
        - Add new error rules using structured arguments
        - Enable or disable error rules for specified application groups
        - Retrieve current error rules for an application group
        - Delete error rules as needed
        - Internal support for XML generation and job status modification

    #ai-gen-doc
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize an _ErrorRule instance for managing job error decision rules.

        Args:
            commcell: Instance of the Commcell class representing the Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> error_rule = _ErrorRule(commcell)
            >>> # The error_rule object can now be used to manage job error rules

        #ai-gen-doc
        """
        self.commcell = commcell
        self.rule_dict = {}
        self.xml_body = """
        <App_SetJobErrorDecision>
        <entity _type_="1" commCellId="{commcell_id}" commCellName="{commserv_name}" />
        <jobErrorRuleList>
        <idaRuleList isEnabled="{enable_flag_ida}">
        <ida _type_="78" appGroupId="57" appGroupName="{app_group_name}" />
        <ruleList>{final_str}<srcEntity _type_="1" commCellId="{commcell_id}" /></ruleList>
        <osEntity _type_="161" />
        </idaRuleList>
        </jobErrorRuleList>
        </App_SetJobErrorDecision>
        """

        self.error_rule_str = """
        <ruleList blockedFileTypes="0" isEnabled="{is_enabled}" jobDecision="{job_decision}" pattern="{pattern}" skipTLbackups="0" skipofflineDBs="0" skippedFiles="0">
        <errorCode allErrorCodes="{all_error_codes}" fromValue="{from_error_code}" skipReportingError="{skip_reporting_error}" toValue="{to_error_code}" />
        </ruleList>
        """

    def _get_xml_for_rule(self, rule_dict: Dict[str, Any]) -> str:
        """Generate the XML string for a rule based on its key-value dictionary.

        This method formats the rule information into an XML string, which is used internally
        when adding new rules or updating existing ones.

        Args:
            rule_dict: Dictionary containing the rule's key-value pairs. Expected keys include:
                - 'pattern': The error pattern to match.
                - 'all_error_codes': Indicates if all error codes are included.
                - 'from_error_code': Starting error code for the rule.
                - 'to_error_code': Ending error code for the rule.
                - 'job_decision': Decision to be taken for the job.
                - 'is_enabled': Whether the rule is enabled.
                - 'skip_reporting_error': Whether to skip reporting the error.

        Returns:
            The XML output formatted as a string.

        Example:
            >>> rule_dict = {
            ...     'pattern': 'ERROR_*',
            ...     'all_error_codes': True,
            ...     'from_error_code': 100,
            ...     'to_error_code': 200,
            ...     'job_decision': 'Fail',
            ...     'is_enabled': True,
            ...     'skip_reporting_error': False
            ... }
            >>> xml_str = error_rule._get_xml_for_rule(rule_dict)
            >>> print(xml_str)
            # The output will be an XML string representing the rule

        #ai-gen-doc
        """

        return self.error_rule_str.format(
            pattern=rule_dict['pattern'],
            all_error_codes=rule_dict['all_error_codes'],
            from_error_code=rule_dict['from_error_code'],
            to_error_code=rule_dict['to_error_code'],
            job_decision=rule_dict['job_decision'],
            is_enabled=rule_dict['is_enabled'],
            skip_reporting_error=rule_dict['skip_reporting_error'])

    def add_error_rule(self, rules_arg: Dict[Any, Dict[str, Dict[str, Any]]]) -> None:
        """Add new error rules or update existing ones for specified application groups.

        This method allows you to add new error rules or update existing rules for each application group.
        Each rule is identified by its rule name and must include specific key-value pairs describing the rule's behavior.

        Args:
            rules_arg: A dictionary where each key is an application group (typically an ApplicationGroup enum constant),
                and the value is another dictionary mapping rule names to rule definitions.
                Each rule definition is itself a dictionary containing the following keys:
                    - appGroupName (Any): The application group name (usually an ApplicationGroup enum constant).
                    - pattern (str): File pattern for the error rule.
                    - all_error_codes (bool): Whether all error codes should be enabled.
                    - from_error_code (int): Lower bound of the error code range (non-negative integer).
                    - to_error_code (int): Upper bound of the error code range (non-negative integer, greater than from_error_code).
                    - job_decision (int): Decision code for the job (typically 0, 1, or 2).
                    - is_enabled (bool): Whether the rule is enabled.
                    - skip_reporting_error (bool): Whether error codes should be skipped from reporting.

        Raises:
            Exception: If invalid key/value pairs are provided in the rule definitions.

        Example:
            >>> rules = {
            ...     WINDOWS: {
            ...         'rule_1': {
            ...             'appGroupName': WINDOWS,
            ...             'pattern': "*",
            ...             'all_error_codes': False,
            ...             'from_error_code': 1,
            ...             'to_error_code': 2,
            ...             'job_decision': 0,
            ...             'is_enabled': True,
            ...             'skip_reporting_error': False
            ...         },
            ...         'rule_2': {
            ...             # Additional rule definition
            ...         }
            ...     }
            ... }
            >>> error_rule_mgr = _ErrorRule(...)
            >>> error_rule_mgr.add_error_rule(rules)
            >>> # This will add or update the specified error rules for the WINDOWS application group.

        #ai-gen-doc
        """

        final_str = ""
        old_values = []

        for app_group, rules_dict in rules_arg.items():
            assert (app_group.name in [i.name for i in ApplicationGroup])

            # FETCH ALL EXISTING RULES ON THE COMMCELL FOR THE APPLICATION
            # GROUP IN QUESTION
            existing_error_rules = self._get_error_rules(app_group)

            for rule_name, rule in rules_dict.items():
                assert isinstance(
                    rule['pattern'], str) and isinstance(
                    rule['all_error_codes'], bool) and isinstance(
                    rule['skip_reporting_error'], int) and isinstance(
                    rule['from_error_code'], int) and isinstance(
                    rule['to_error_code'], int) and isinstance(
                    rule['job_decision'], int) and rule['job_decision'] in range(
                    0, 3) and isinstance(
                    rule['is_enabled'], bool), "Invalid key value pairs provided."

                rule_dict = {k:v for k,v in rule.items() if k != 'appGroupName'}

                # GET RULE STRING FOR EACH RULE DICTIONARY PROVIDED IN THE ARGUMENT
                new_rule_str = self._get_xml_for_rule(rule_dict)

                # IF RULE NAME NOT PRESENT IN OUR INTERNAL STRUCTURE, IT MEANS USER IS ADDING NEW RULE
                if rule_name not in list(self.rule_dict.keys()):
                    self.rule_dict[rule_name] = {'new_value': new_rule_str, 'old_value': new_rule_str}
                    final_str = ''.join((final_str, new_rule_str))

                # ELSE CHECK IF THE RULE'S VALUE REMAINS SAME AND IF IT DOES, WE SIMPLY CONTINUE AND STORE EXISTING VALUE
                elif new_rule_str == self.rule_dict[rule_name]['old_value']:
                    final_str = ''.join((final_str, self.rule_dict[rule_name]['old_value']))

                # ELSE RULE IS BEING UPDATED, STORE NEW VALUE IN FINAL STRING AND PRESERVE OLD VALUE AS WELL
                else:
                    self.rule_dict[rule_name]['old_value'] = self.rule_dict[rule_name]['new_value']
                    self.rule_dict[rule_name]['new_value'] = new_rule_str
                    final_str = ''.join((final_str, new_rule_str))

            # NOW GO THROUGH ALL EXISTING RULES ON CS AND EITHER PRESERVE OR UPDATE IT
            # PREPARE A LIST OF ALL OLD VALUES FIRST
            for rule_name, values in self.rule_dict.items():
                old_values.extend([value for value_type, value in values.items() if value_type == 'old_value'])
            for existing_error_rule in existing_error_rules:
                existing_rule_dict = {'pattern': existing_error_rule['pattern'],
                                      'all_error_codes': existing_error_rule['errorCode']['allErrorCodes'],
                                      'skip_reporting_error': existing_error_rule['errorCode']['skipReportingError'],
                                      'from_error_code': existing_error_rule['errorCode']['fromValue'],
                                      'to_error_code': existing_error_rule['errorCode']['toValue'],
                                      'job_decision': existing_error_rule['jobDecision'],
                                      'is_enabled': existing_error_rule['isEnabled']}

                existing_rule_str = self._get_xml_for_rule(existing_rule_dict)
                # AN EXISTING RULE THAT HAS NOT BEEN UPDATED AND IS NOT ADDED BY THE TEST CASE OR THROUGH AUTOMATION.
                # IN OTHER WORDS, AN EXISTING RULE THAT WAS ADDED OUTSIDE OF THE SCOPE OF THE TEST CASE
                if existing_rule_str not in old_values:
                    final_str = ''.join((final_str, existing_rule_str))

        # NEED TO ADD SUPPORT FOR UPDATION OF ERROR RULES FOR MULTIPLE iDAs SIMULTANEOUSLY
        xml_body = self.xml_body.format(commcell_id=self.commcell.commcell_id,
                                        commserv_name=self.commcell.commserv_name,
                                        enable_flag_ida=1,
                                        app_group_name=app_group,
                                        final_str=final_str)

        xml_body = ''.join(i.lstrip().rstrip() for i in xml_body.split("\n"))
        self.commcell.qoperation_execute(xml_body)

    def enable(self, app_group: str) -> None:
        """Enable job error control rules for the specified Application Group Type.

        This method sets the enable flag for job error control rules associated with the given application group.

        Args:
            app_group: The application group identifier (iDA) for which the enable flag should be set.
                Example supported value: "APPGRP_WindowsFileSystemIDA".

        Example:
            >>> error_rule = _ErrorRule()
            >>> error_rule.enable("APPGRP_WindowsFileSystemIDA")
            >>> print("Error control rules enabled for Windows File System iDA")

        #ai-gen-doc
        """
        return self._modify_job_status_on_errors(app_group, enable_flag=True)

    def disable(self, app_group: str) -> None:
        """Disable job error control rules for the specified Application Group Type.

        Args:
            app_group: The iDA (Intelligent Data Agent) name for which the error control rules should be disabled.
                Supported values include "APPGRP_WindowsFileSystemIDA".

        Example:
            >>> error_rule = _ErrorRule()
            >>> error_rule.disable("APPGRP_WindowsFileSystemIDA")
            >>> print("Error control rules disabled for Windows File System iDA")

        #ai-gen-doc
        """
        return self._modify_job_status_on_errors(app_group, enable_flag=False)

    def _modify_job_status_on_errors(self, app_group: str, enable_flag: bool):
        """Enable or disable job status updates based on error rules for a specific iDA.

        This method updates the job status behavior for the specified application group (iDA)
        by enabling or disabling job status on errors according to the current error rules.

        Args:
            app_group: The iDA (application group) for which the enable flag should be set.
                Example value: "APPGRP_WindowsFileSystemIDA".
            enable_flag: If True, enables job status updates on errors; if False, disables them.

        Example:
            >>> error_rule = _ErrorRule(commcell)
            >>> error_rule._modify_job_status_on_errors("APPGRP_WindowsFileSystemIDA", True)
            >>> # Job status on errors is now enabled for Windows File System iDA

        #ai-gen-doc
        """

        # FETCHING ALL EXISTING RULES
        error_rules = self._get_error_rules(app_group)

        # FOR EVERY RULE IN RULE LIST
        for rule in error_rules:
            rule_str = self.error_rule_str.format(pattern=rule['pattern'],
                                                  all_error_codes=rule['errorCode']['allErrorCodes'],
                                                  from_error_code=rule['errorCode']['fromValue'],
                                                  to_error_code=rule['errorCode']['toValue'],
                                                  job_decision=rule['jobDecision'],
                                                  is_enabled=rule['isEnabled'],
                                                  skip_reporting_error=rule['errorCode']['skipReportingError'])

            final_str = ''.join((final_str, rule_str))

        xml_body = self.xml_body.format(commcell_id=self.commcell.commcell_id,
                                        commserv_name=self.commcell.commserv_name,
                                        enable_flag_ida=1 if enable_flag else 0,
                                        final_str=final_str)

        xml_body = ''.join(i.lstrip().rstrip() for i in xml_body.split("\n"))
        return self.commcell.qoperation_execute(xml_body)

    def _get_error_rules(self, app_group: str) -> List[Dict[str, Any]]:
        """Retrieve error rules configured on the CommServe for a specific application group.

        Args:
            app_group: The application group (iDA) name for which error rules are to be fetched.
                Example: "APPGRP_WindowsFileSystemIDA"

        Returns:
            A list of error rule dictionaries. Each dictionary contains key-value pairs such as pattern,
            error code range, and other rule attributes.

        Example:
            >>> error_rule_obj = _ErrorRule()
            >>> rules = error_rule_obj._get_error_rules("APPGRP_WindowsFileSystemIDA")
            >>> for rule in rules:
            ...     print(rule)
            >>> # Each rule is a dictionary with error pattern and code details

        #ai-gen-doc
        """

        rule_list = []

        xml_body = f"""
        <App_GetJobErrorDecisionReq>
        <entity _type_="1" commCellId="{self.commcell.commcell_id}" commCellName="{self.commcell.commserv_name}"/>
        </App_GetJobErrorDecisionReq>"""

        xml_body = ''.join(i.lstrip().rstrip() for i in xml_body.split("\n"))
        error_rules = self.commcell.qoperation_execute(xml_body)

        if any(error_rules):

            ida_rule_lists = error_rules['jobErrorRuleList']['idaRuleList']
            for ida_rule_list in ida_rule_lists:
                # HARD CODED FOR WINDOWS SUPPORT ONLY
                if ida_rule_list['ida']['appGroupName'] == app_group:
                    try:
                        rule_list = ida_rule_list['ruleList']['ruleList']
                    except Exception:
                        pass

        return rule_list
