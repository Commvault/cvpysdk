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


class JobController(object):
    """Class for controlling all the jobs associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize instance of the JobController class to get the details of Commcell Jobs.

            Args:
                commcell_object     (object)    --  instance of Commcell class to get the jobs of

            Returns:
                None

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

    def __str__(self):
        """Representation string consisting of all active jobs on this commcell.

            Returns:
                str     -   string of all the active jobs on this commcell

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

    def __repr__(self):
        """Representation string for the instance of the JobController class."""
        return "JobController class instance for Commcell"

    def _get_jobs_request_json(self, **options):
        """Returns the request json for the jobs request

            Args:
                options     (dict)  --  dict of key-word arguments

                Available Options:

                    category        (str)   --  category name for which the list of jobs
                    are to be retrieved

                        Valid Values:

                            - ALL

                            - ACTIVE

                            - FINISHED

                        default: ALL

                    limit           (int)   --  total number of jobs list that are to be returned

                            default: 20

                    offset           (int)  --  value from which starting job to be returned is counted

                            default: 0

                    lookup_time     (int)   --  list of jobs to be retrieved which are specified
                    hours older

                            default: 5 hours

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                            default: False
                    
                    hide_admin_jobs (bool)  --  boolean specifying whether to exclude admin jobs from
                    the result or not

                            default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                            default: []

                    job_type_list   (list)  --  list of job operation types

                            default: []

                    entity          (dict)  --  dict containing entity details to which associated jobs has to be fetched

                            Example : To fetch job details of particular data source id

                                "entity": {
                                            "dataSourceId": 2575
                                            }


            Returns:
                dict    -   request json that is to be sent to server

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

    def _get_jobs_list(self, **options):
        """Executes a request on the server to get the list of jobs.

            Args:
                request_json    (dict)  --  request that is to be sent to server

            Returns:
                dict    -   dict containing details about all the retrieved jobs

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def _modify_all_jobs(self, operation_type=None):
        """ Executes a request on the server to suspend/resume/kill all the jobs on the commserver

            Args:
                operation_type     (str)   --  All jobs on commcell will be changed to this
                                                    state.
                                                    Options:
                                                        suspend/resume/kill

            Returns:
                None

            Raises:
                SDKException:
                    - Invalid input is passed to the module

                    - Failed to execute the api to modify jobs

                    - Response is incorrect
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

    def all_jobs(self, client_name=None, lookup_time=5, job_filter=None, **options):
        """Returns the dict consisting of all the jobs executed on the Commcell within the number
            of hours specified in lookup time value.

            Args:
                client_name     (str)   --  name of the client to filter out the jobs for

                    default: None, get all the jobs


                lookup_time     (int)   --  get all the jobs executed within the number of hours

                    default: 5 Hours


                job_filter      (str)   --  type of jobs to filter

                        for multiple filters, give the values **comma(,)** separated

                        List of Possible Values:

                            Backup

                            Restore

                            AUXCOPY

                            WORKFLOW

                            etc..

                    http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm
                        to get the complete list of filters available

                    default: None

                options         (dict)  --  dict of key-word arguments

                Available Options:

                    limit           (int)   --  total number of jobs list that are to be returned
                        default: 20

                    offset           (int)  --  value from which starting job to be returned is counted

                        default: 0

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                        default: False

                    hide_admin_jobs (bool)  --  boolean specifying whether to exclude admin jobs from
                    the result or not

                        default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                        default: []

                    job_type_list   (list)  --  list of job operation types

                        default: []

                    job_summary     (str)   --  To return the basic job summary or full job summary

                        default: basic

                        accepted values: ['basic', 'full']

            Returns:
                dict    -   dictionary consisting of the job IDs matching the given criteria
                as the key, and their details as its value

            Raises:
                SDKException:
                    if client name is given, and no client exists with the given name

        """
        options['category'] = 'ALL'
        options['lookup_time'] = lookup_time

        if job_filter:
            options['job_type_list'] = options.get('job_type_list', []) + job_filter.split(',')

        if client_name:
            options['clients_list'] = options.get('clients_list', []) + [client_name]

        return self._get_jobs_list(**options)

    def active_jobs(self, client_name=None, lookup_time=1, job_filter=None, **options):
        """Returns the dict consisting of all the active jobs currently being executed on the
            Commcell within the number of hours specified in lookup time value.

            Args:
                client_name     (str)   --  name of the client to filter out the jobs for

                    default: None, get all the jobs


                lookup_time     (int)   --  get all the jobs executed within the number of hours

                    default: 1 Hour(s)


                job_filter      (str)   --  type of jobs to filter

                        for multiple filters, give the values **comma(,)** separated

                        List of Possible Values:

                            Backup

                            Restore

                            AUXCOPY

                            WORKFLOW

                            etc..

                    http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm
                        to get the complete list of filters available

                    default: None

                options         (dict)  --  dict of key-word arguments

                Available Options:

                    limit           (int)   --  total number of jobs list that are to be returned

                        default: 20

                    offset          (int)   --  value from which starting job to be returned is counted

                        default: 0

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                        default: False

                    hide_admin_jobs (bool)  --  boolean specifying whether to exclude admin jobs from
                    the result or not

                        default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                        default: []

                    job_type_list   (list)  --  list of job operation types

                        default: []

                    job_summary     (str)   --  To return the basic job summary or full job summary

                        default: basic

                        accepted values: ['basic', 'full']

                    entity          (dict)  --  dict containing entity details to which associated jobs has to be fetched

                        Example : To fetch job details of particular data source id

                                "entity": {
                                            "dataSourceId": 2575
                                            }

            Returns:
                dict    -   dictionary consisting of the job IDs matching the given criteria
                as the key, and their details as its value

            Raises:
                SDKException:
                    if client name is given, and no client exists with the given name

        """
        options['category'] = 'ACTIVE'
        options['lookup_time'] = lookup_time

        if job_filter:
            options['job_type_list'] = options.get('job_type_list', []) + job_filter.split(',')

        if client_name:
            options['clients_list'] = options.get('clients_list', []) + [client_name]

        return self._get_jobs_list(**options)

    def finished_jobs(self, client_name=None, lookup_time=24, job_filter=None, **options):
        """Returns the dict consisting of all the finished jobs on the Commcell within the number
            of hours specified in lookup time value.

            Args:
                client_name     (str)   --  name of the client to filter out the jobs for

                    default: None, get all the jobs ir-respective of client


                lookup_time     (int)   --  get all the jobs executed within the number of hours

                    default: 24 Hours


                job_filter      (str)   --  type of jobs to filter

                        for multiple filters, give the values **comma(,)** separated

                        List of Possible Values:

                            Backup

                            Restore

                            AUXCOPY

                            WORKFLOW

                            etc..

                    http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm
                        to get the complete list of filters available

                    default: None


                options         (dict)  --  dict of key-word arguments

                Available Options:

                    limit           (int)   --  total number of jobs list that are to be returned

                        default: 20

                    offset          (int)   --  value from which starting job to be returned is counted

                            default: 0

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                        default: False

                    hide_admin_jobs (bool)  --  boolean specifying whether to exclude admin jobs from
                    the result or not

                        default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                        default: []

                    job_type_list   (list)  --  list of job operation types

                        default: []

                    job_summary     (str)   --  To return the basic job summary or full job summary

                        default: basic

                        accepted values: ['basic', 'full']

                    entity          (dict)  --  dict containing entity details to which associated jobs has to be fetched

                        Example : To fetch job details of particular data source id

                                "entity": {
                                            "dataSourceId": 2575
                                            }

            Returns:
                dict    -   dictionary consisting of the job IDs matching the given criteria
                as the key, and their details as its value

            Raises:
                SDKException:
                    if client name is given, and no client exists with the given name

        """
        options['category'] = 'FINISHED'
        options['lookup_time'] = lookup_time

        if job_filter:
            options['job_type_list'] = options.get('job_type_list', []) + job_filter.split(',')

        if client_name:
            options['clients_list'] = options.get('clients_list', []) + [client_name]

        return self._get_jobs_list(**options)

    def suspend_all_jobs(self):
        """ Suspends all the jobs on the commserver """
        self._modify_all_jobs('suspend')

    def resume_all_jobs(self):
        """ Resumes all the jobs on the commserver """
        self._modify_all_jobs('resume')

    def kill_all_jobs(self):
        """ Kills all the jobs on the commserver """
        self._modify_all_jobs('kill')

    def get(self, job_id):
        """Returns the job object for the given job id.

            Args:
                job_id  (int)   --  id of the job to create Job class instance for

            Returns:
                object  -   Job class object for the given job id

            Raises:
                SDKException:
                    if no job with specified job id exists

        """
        return Job(self._commcell_object, job_id)


class JobManagement(object):
    """Class for performing job management operations. """

    def __init__(self, commcell_object):
        """
        Initialize instance of JobManagement class for performing operations on jon management settings.

            Args:
                commcell_object         (object)        --  instance of Commcell class.

            Returns:
                None

        """
        self._comcell = commcell_object
        self._service = commcell_object._services.get('JOB_MANAGEMENT_SETTINGS')
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._error_rules = None
        self.refresh()

    @property
    def error_rules(self):
        if not self._error_rules:
            self._error_rules = _ErrorRule(self._comcell)
        return self._error_rules

    def _set_jobmanagement_settings(self):
        """
        Executes a request on the server, to set the job management settings.

         Returns:
               None

         Raises:
              SDKException:
                    if given inputs are invalid

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

    def _get_jobmanagement_settings(self):
        """
         Executes a request on the server to get the settings of job management.

            Returns:
                None

            Raises:
                SDKException
                    if response is empty

                    if response is not success
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

    def refresh(self):
        """
        calls the private method _get_jobmanagement_settings()
        """
        self._restart_settings = None
        self._general_settings = None
        self._update_settings = None
        self._priority_settings = None
        self._get_jobmanagement_settings()

    def set_general_settings(self, settings):
        """
        sets general settings of job management.

        Note : dedicated setters and getters are provided for general settings.
            Args:
                settings (dict)  --       Following key/value pairs can be set.
                                            {
                                                "allowRunningJobsToCompletePastOperationWindow": False,
                                                "jobAliveCheckIntervalInMinutes": 5,
                                                "queueScheduledJobs": False,
                                                "enableJobThrottleAtClientLevel": False,
                                                "enableMultiplexingForDBAgents": False,
                                                "queueJobsIfConflictingJobsActive": False,
                                                "queueJobsIfActivityDisabled": False,
                                                "backupsPreemptsAuxilaryCopy": False,
                                                "restorePreemptsOtherJobs": False,
                                                "enableMultiplexingForOracle": False,
                                                "jobStreamHighWaterMarkLevel": 500,
                                                "backupsPreemptsOtherBackups": False,
                                                "doNotStartBackupsOnDisabledClient": False

                                            }
            Returns:
                None

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(settings, dict):
            self._general_settings.get('generalSettings').update(settings)
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    def set_priority_settings(self, settings):
        """
        sets priority settings for jobs and agents type.

            Args:
                settings  (list)    --  list of dictionaries with following format.
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

            We have priority settings fro jobtype and agenttype

            NOTE : for setting, priority for jobtype the 'type_of_operation' must be set to 1 and name of the job type
                   must be specified as below format.

                       ex :-  "jobTypeName": "Information Management"

            NOTE : for setting, priority for agenttype the 'type_of_operation' must be set to 2 and name of the job
             type must be specified as below format

                        ex :- "appTypeName": "Windows File System"

            Returns:
                None

            Raises:
                SDKException:
                    if input is not valid type

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

    def set_restart_settings(self, settings):
        """
        sets restart settings for jobs.

            Args:
                settings    (list)      --  list of dictionaries with following format
                                            [
                                                {
                                                    "killRunningJobWhenTotalRunningTimeExpires": False,
                                                    "maxRestarts": 10,
                                                    "enableTotalRunningTime": False,
                                                    "restartable": False,
                                                    "jobTypeName": "File System and Indexing Based (Data Protection)",
                                                    "restartIntervalInMinutes": 20,
                                                    "preemptable": True,
                                                    "totalRunningTime": 21600,
                                                    "jobType": 6
                                                },
                                                {
                                                    "killRunningJobWhenTotalRunningTimeExpires": False,
                                                    "maxRestarts": 144,
                                                    "enableTotalRunningTime": False,
                                                    "restartable": False,
                                                    "jobTypeName": "File System and Indexing Based (Data Recovery)",
                                                    "restartIntervalInMinutes": 20,
                                                    "preemptable": False,
                                                    "totalRunningTime": 21600,
                                                    "jobType": 7
                                                }
                                            ]

            Returns:
                None

            Raises:
                SDKException:
                    if input is not valid type

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

    def set_update_settings(self, settings):
        """
        sets update settings for jobs

            Args:
                settings    (list)      --      list of dictionaries with following format
                                                [
                                                    {
                                                        "appTypeName": "Windows File System",
                                                        "recoveryTimeInMinutes": 20,
                                                        "protectionTimeInMinutes": 20
                                                    },
                                                    {
                                                        "appTypeName": "Windows XP 64-bit File System",
                                                        "recoveryTimeInMinutes": 20,
                                                        "protectionTimeInMinutes": 20,
                                                    }
                                                ]
            Returns:
                None

            Raises:
                SDKException:
                    if input is not valid type

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
    def job_priority_precedence(self):
        """
        gets the job priority precedence
            Returns:
                 (str)  --   type of job priority precedence is set.
        """

        available_priorities = {
            1: "client",
            2: "agentType"
        }
        return available_priorities.get(self._priority_settings["jobPrioritySettings"]["priorityPrecedence"])

    @job_priority_precedence.setter
    def job_priority_precedence(self, priority_type):
        """
        sets job priority precedence

                Args:
                    priority_type   (str)   --      type of priority to be set

                    Values:
                        "client"
                        "agentType"

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
    def start_phase_retry_interval(self):
        """
        gets the start phase retry interval in (minutes)
            Returns:
                 (int)      --      interval in minutes.
        """
        return self._restart_settings["jobRestartSettings"]["startPhaseRetryIntervalInMinutes"]

    @start_phase_retry_interval.setter
    def start_phase_retry_interval(self, minutes):
        """
        sets start phase retry interval for jobs

            Args:
                minutes     (int)       --      minutes to be set.

            Raises:
                SDKException:
                    if input is not valid type.
        """

        if isinstance(minutes, int):
            self._restart_settings["jobRestartSettings"]["startPhaseRetryIntervalInMinutes"] = minutes
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    @property
    def state_update_interval_for_continuous_data_replicator(self):
        """
        gets the state update interval for continuous data replicator in (minutes)
            Returns:
                 (int)      --      interval in minutes
        """
        return self._update_settings["jobUpdatesSettings"]["stateUpdateIntervalForContinuousDataReplicator"]

    @state_update_interval_for_continuous_data_replicator.setter
    def state_update_interval_for_continuous_data_replicator(self, minutes):
        """
        sets state update interval for continuous data replicator

            Args:
                 minutes       (int)        --      minutes to be set.

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(minutes, int):
            self._update_settings["jobUpdatesSettings"]["stateUpdateIntervalForContinuousDataReplicator"] = minutes
            self._set_jobmanagement_settings()
        else:
            raise SDKException('Job', '108')

    @property
    def allow_running_jobs_to_complete_past_operation_window(self):
        """
        Returns True if option is enabled
        else returns false
        """
        return self._general_settings.get('generalSettings').get("allowRunningJobsToCompletePastOperationWindow")

    @allow_running_jobs_to_complete_past_operation_window.setter
    def allow_running_jobs_to_complete_past_operation_window(self, flag):
        """
        enable/disable, allow running jobs to complete past operation window.
            Args:
                flag    (bool)    --        (True/False) to be set.

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "allowRunningJobsToCompletePastOperationWindow": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def job_alive_check_interval_in_minutes(self):
        """
        gets the job alive check interval in (minutes)
            Returns:
                (int)       --      interval in minutes
        """
        return self._general_settings.get('generalSettings').get("jobAliveCheckIntervalInMinutes")

    @job_alive_check_interval_in_minutes.setter
    def job_alive_check_interval_in_minutes(self, minutes):
        """
        sets the job alive check interval in (minutes)
            Args:
                  minutes       --      minutes to be set.

            Raises:
                  SDKException:
                        if input is not valid type
        """
        if isinstance(minutes, int):
            settings = {
                "jobAliveCheckIntervalInMinutes": minutes
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def queue_scheduled_jobs(self):
        """
        Returns True if option is enabled
        else returns false
        """
        return self._general_settings.get('generalSettings').get("queueScheduledJobs")

    @queue_scheduled_jobs.setter
    def queue_scheduled_jobs(self, flag):
        """
        enable/disable, queue scheduled jobs

            Args:
                flag   (bool)      --       (True/False to be set)

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "queueScheduledJobs": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def enable_job_throttle_at_client_level(self):
        """
        Returns True if option is enabled
        else returns false
        """
        return self._general_settings.get('generalSettings').get("enableJobThrottleAtClientLevel")

    @enable_job_throttle_at_client_level.setter
    def enable_job_throttle_at_client_level(self, flag):
        """
        enable/disable, job throttle at client level
            Args:
                flag    (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "enableJobThrottleAtClientLevel": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def enable_multiplexing_for_db_agents(self):
        """
        Returns True if option is enabled
        else returns False
        """
        return self._general_settings.get('generalSettings').get("enableMultiplexingForDBAgents")

    @enable_multiplexing_for_db_agents.setter
    def enable_multiplexing_for_db_agents(self, flag):
        """
        enable/disable, multiplexing for db agents
            Args:
                flag    (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "enableMultiplexingForDBAgents": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def queue_jobs_if_conflicting_jobs_active(self):
        """
        Returns True if option is enabled
        else returns false
        """
        return self._general_settings.get('generalSettings').get("queueJobsIfConflictingJobsActive")

    @queue_jobs_if_conflicting_jobs_active.setter
    def queue_jobs_if_conflicting_jobs_active(self, flag):
        """
        enable/disable, queue jobs if conflicting jobs active
            Args;
                flag    (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "queueJobsIfConflictingJobsActive": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def queue_jobs_if_activity_disabled(self):
        """
        Returns True if option is enabled
        else returns False
        """
        return self._general_settings.get('generalSettings').get("queueJobsIfActivityDisabled")

    @queue_jobs_if_activity_disabled.setter
    def queue_jobs_if_activity_disabled(self, flag):
        """
        enable/disable, queue jobs if activity disabled
            Args;
                flag    (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "queueJobsIfActivityDisabled": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def backups_preempts_auxilary_copy(self):
        """
        Returns True if option is enabled
        else returns False
        """
        return self._general_settings.get('generalSettings').get("backupsPreemptsAuxilaryCopy")

    @backups_preempts_auxilary_copy.setter
    def backups_preempts_auxilary_copy(self, flag):
        """
        enable/disable, backups preempts auxiliary copy
            Args:
                flag    (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "backupsPreemptsAuxilaryCopy": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def restore_preempts_other_jobs(self):
        """
        Returns True if option is enabled
        else returns False
        """
        return self._general_settings.get('generalSettings').get("restorePreemptsOtherJobs")

    @restore_preempts_other_jobs.setter
    def restore_preempts_other_jobs(self, flag):
        """
        enable/disable, restore preempts other jobs
            Args:
                flag    (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "restorePreemptsOtherJobs": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def enable_multiplexing_for_oracle(self):
        """
        Returns True if option is enabled
        else returns False
        """
        return self._general_settings.get('generalSettings').get("enableMultiplexingForOracle")

    @enable_multiplexing_for_oracle.setter
    def enable_multiplexing_for_oracle(self, flag):
        """
        enable/disable, enable multiplexing for oracle
            Args:
                 flag   (bool)  --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(flag, bool):
            settings = {
                "enableMultiplexingForOracle": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def job_stream_high_water_mark_level(self):
        """
        gets the job stream high water mark level
        """
        return self._general_settings.get('generalSettings').get("jobStreamHighWaterMarkLevel")

    @job_stream_high_water_mark_level.setter
    def job_stream_high_water_mark_level(self, level):
        """
        sets, job stream high water mak level
            Args:
                level   (int)       --      number of jobs to be performed at a time

            Raises:
                SDKException:
                    if input is not valid type
        """
        if isinstance(level, int):
            settings = {
                "jobStreamHighWaterMarkLevel": level
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def backups_preempts_other_backups(self):
        """
        Returns True if option is enabled
        else returns False
        """
        return self._general_settings.get('generalSettings').get("backupsPreemptsOtherBackups")

    @backups_preempts_other_backups.setter
    def backups_preempts_other_backups(self, flag):
        """
        enable/disable, backups preempts other backups
            Args:
                 flag   (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not a valid type
        """
        if isinstance(flag, bool):
            settings = {
                "backupsPreemptsOtherBackups": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    @property
    def do_not_start_backups_on_disabled_client(self):
        """
        Returns True if option is enabled
        else returns False
        """
        return self._general_settings.get('generalSettings').get("doNotStartBackupsOnDisabledClient")

    @do_not_start_backups_on_disabled_client.setter
    def do_not_start_backups_on_disabled_client(self, flag):
        """
         enable/disable, do not start backups on disabled client
            Args:
                 flag   (bool)      --      (True/False) to be set

            Raises:
                SDKException:
                    if input is not a valid type
        """
        if isinstance(flag, bool):
            settings = {
                "doNotStartBackupsOnDisabledClient": flag
            }
            self.set_general_settings(settings)
        else:
            raise SDKException('Job', '108')

    def get_restart_setting(self, jobtype):
        """
        restart settings associated to particular jobtype can be obtained
            Args:
                jobtype     (str)       --      settings of the jobtype to get

                Available jobtypes:

                        "Disaster Recovery backup"
                        "Auxiliary Copy"
                        "Data Aging"
                        "Download/Copy Updates"
                        "Offline Content Indexing"
                        "Information Management"
                        "File System and Indexing Based (Data Protection)"
                        "File System and Indexing Based (Data Recovery)"
                        "Exchange DB (Data Protection)"
                        "Exchange DB (Data Recovery)"
                        "Informix DB (Data Protection)"
                        "Informix DB (Data Recovery)"
                        "Lotus Notes DB (Data Protection)"
                        "Lotus Notes DB (Data Recovery)"
                        "Oracle DB (Data Protection)"
                        "Oracle DB (Data Recovery)"
                        "SQL DB (Data Protection)"
                        "SQL DB (Data Recovery)"
                        "MYSQL (Data Protection)"
        `               "MYSQL (Data Recovery)"
                        "Sybase DB (Data Protection)"
                        "Sybase DB (Data Recovery)"
                        "DB2 (Data Protection)"
                        "DB2 (Data Recovery)"
                        "CDR (Data Management)"
                        "Media Refresh"
                        "Documentum (Data Protection)"
                        "Documentum (Data Recovery)"
                        "SAP for Oracle (Data Protection)"
                        "SAP for Oracle (Data Recovery)"
                        "PostgreSQL (Data Protection)"
                        "PostgreSQL (Data Recovery)"
                        "Other (Data Protection)"
                        "Other (Data Recovery)"
                        "Workflow"
                        "DeDup DB Reconstruction"
                        "CommCell Migration Export"
                        "CommCell Migration Import"
                        "Install Software"
                        "Uninstall Software"
                        "Data Verification"
                        "Big Data Apps (Data Protection)"
                        "Big Data Apps (Data Recovery)"
                        "Cloud Apps (Data Protection)"
                        "Cloud Apps (Data Recovery)"
                        "Virtual Server (Data Protection)"
                        "Virtual Server (Data Recovery)"
                        "SAP for Hana (Data Protection)"
                        "SAP for Hana (Data Recovery)"



            Returns:
                dict          --        settings of the specific job type as follows
                                        {
                                            "jobTypeName": "File System and Indexing Based (Data Protection)",
                                            "restartable": true,
                                            "maxRestarts": 10,
                                            "restartIntervalInMinutes": 20,
                                            "enableTotalRunningTime": false,
                                            "totalRunningTime": 25200,
                                            "killRunningJobWhenTotalRunningTimeExpires": false,
                                            "preemptable": true,

                                        }

            Raises:
                SDKException:
                    if input is not valid type

        """
        if isinstance(jobtype, str):
            for job_type in self._restart_settings['jobRestartSettings']['jobTypeRestartSettingList']:
                if job_type['jobTypeName'] == jobtype:
                    settings = copy.deepcopy(job_type)
                    return settings
        else:
            raise SDKException('Job', '108')

    def get_priority_setting(self, jobtype):
        """
        priority settings associated to particular jobtype can be obtained
            Args:
                jobtype     (str)       --      settings of jobtype to get

                Available values:

                    jobtypename:
                        "Information Management"
                        "Auxiliary Copy"
                        "Media Refresh"
                        "Data Verification"
                        "Persistent Recovery"
                        "Synth Full"

                    apptypename:
                        "Windows File System"
                        "Windows XP 64-bit File System"
                        "Windows 2003 32-bit File System"
                        "Windows 2003 64-bit File System"
                        "Active Directory"
                        "Windows File Archiver"
                        "File Share Archiver"
                        "Image Level"
                        "Exchange Mailbox (Classic)"
                        "Exchange Mailbox Archiver"
                        "Exchange Compliance Archiver"
                        "Exchange Public Folder"
                        "Exchange Database"
                        "SharePoint Database"
                        "SharePoint Server Database"
                        "SharePoint Document"
                        "SharePoint Server"
                        "Novell Directory Services"
                        "GroupWise DB"
                        "NDMP"
                        "Notes Document"
                        "Unix Notes Database"
                        "MAC FileSystem"
                        "Big Data Apps"
                        "Solaris File System"
                        "Solaris 64bit File System"
                        "FreeBSD"
                        "HP-UX File System"
                        "HP-UX 64bit File System"
                        "AIX File System"
                        "Unix Tru64 64-bit File System"
                        "Linux File System"
                        "Sybase Database"
                        "Oracle Database"
                        "Oracle RAC"
                        "Informix Database"
                        "DB2"
                        "DB2 on Unix"
                        "SAP for Oracle"
                        "SAP for MAX DB"
                        "ProxyHost on Unix"
                        "ProxyHost"
                        "Image Level On Unix"
                        "OSSV Plug-in on Windows"
                        "OSSV Plug-in on Unix"
                        "Unix File Archiver"
                        "SQL Server"
                        "Data Classification"
                        "OES File System on Linux"
                        "Centera"
                        "Exchange PF Archiver"
                        "Domino Mailbox Archiver"
                        "MS SharePoint Archiver"
                        "Content Indexing Agent"
                        "SRM Agent For Windows File Systems"
                        "SRM Agent For UNIX File Systems"
                        "DB2 MultiNode"
                        "MySQL"
                        "Virtual Server"
                        "SharePoint Search Connector"
                        "Object Link"
                        "PostgreSQL"
                        "Sybase IQ"
                        "External Data Connector"
                        "Documentum"
                        "Object Store"
                        "SAP HANA"
                        "Cloud Apps"
                        "Exchange Mailbox"

            Returns:
                dict        --          settings of a specific jobtype
                                        ex:
                                        {
                                            "jobTypeName": "Information Management",
                                            "combinedPriority": 0,
                                            "type_of_operation": 1
                                        }

                                        or

                                        settings of a specific apptype
                                        ex:
                                        {
                                            "appTypeName": "Windows File System",
                                            "combinedPriority": 6,
                                            "type_of_operation": 2
                                        }
            Raises:
                SDKException:
                    if input is not valid type

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

    def get_update_setting(self, jobtype):
        """
        update settings associated to particular jobtype can be obtained
            Args:
                jobtype     (str)       --      settings of jobtype to get

                Available jobtype

                    Check get_priority_setting(self, jobtype) method documentation.

            Returns:
                dict        -           settings of a jobtype
                                        {
                                            "appTypeName": "Windows File System",
                                            "recoveryTimeInMinutes": 20,
                                            "protectionTimeInMinutes": 20
                                        }
            Raises:
                SDKException:
                    if input is not valid type

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
    def general_settings(self):
        """
        gets the general settings.
             Returns:   (dict)      --  The general settings
        """
        return self._general_settings

    @property
    def restart_settings(self):
        """
        gets the restart settings.
                Returns:    (dict)    --  The restart settings.
        """

        return self._restart_settings

    @property
    def priority_settings(self):
        """
        gets the priority settings.
                Returns:    (dict)    --  The priority settings.
        """

        return self._priority_settings

    @property
    def update_settings(self):
        """
        gets the update settings.
                Returns:    (dict)    --  The update settings.
        """

        return self._update_settings

    def set_job_error_threshold(self, error_threshold_dict):
        """

        Args:
            error_threshold_dict  (dict)  :   A dictionary of following  key/value pairs can be set.

        Returns:
            None

        """
        raise NotImplementedError("Yet To Be Implemented")


class Job(object):
    """Class for performing client operations for a specific client."""

    def __init__(self, commcell_object, job_id):
        """Initialise the Job class instance.

            Args:
                commcell_object     (object)        --  instance of the Commcell class

                job_id              (str / int)     --  id of the job

            Returns:
                object  -   instance of the Job class

            Raises:
                SDKException:
                    if job id is not an integer

                    if job is not a valid job, i.e., does not exist in the Commcell

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

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str     -   string for instance of this class

        """
        representation_string = 'Job class instance for job id: "{0}"'
        return representation_string.format(self.job_id)

    def _is_valid_job(self):
        """Checks if the job submitted with the job id is a valid job or not.

            Returns:
                bool    -   boolean that represents whether the job is valid or not

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

    def _get_job_summary(self):
        """Gets the properties of this job.

            Returns:
                dict    -   dict that contains the summary of this job

            Raises:
                SDKException:
                    if no record found for this job

                    if response is empty

                    if response is not success

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

    def _get_job_details(self):
        """Gets the detailed properties of this job.

            Returns:
                dict    -   dict consisting of the detailed properties of the job

            Raises:
                SDKException:
                    if failed to get the job details

                    if response is empty

                    if response is not success

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

    def _get_job_task_details(self):
        """Gets the task details of this job.

            Returns:
                dict    -   dict consisting of the task details of the job

            Raises:
                SDKException:
                    if failed to get the job task details

                    if response is empty

                    if response is not success

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

    def _initialize_job_properties(self):
        """Initializes the common properties for the job.
            Adds the client, agent, backupset, subclient name to the job object.

        """
        self._summary = self._get_job_summary()
        self._details = self._get_job_details()

        self._status = self._summary['status']

        self._start_time = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.gmtime(self._summary['jobStartTime'])
        )

    def _wait_for_status(self, status, timeout=6):
        """Waits for 6 minutes or till the job status is changed to given status,
            whichever is earlier.

            Args:
                status  (str)   --  Job Status

                timeout (int)   --  timeout interval in mins

            Returns:
                None

        """
        start_time = time.time()
        current_job_status = self.status
        current_job_status = current_job_status if current_job_status else self.state
        while current_job_status.lower() != status.lower():
            if (self.is_finished is True) or (time.time() - start_time > (timeout * 60)):
                break

            time.sleep(3)
            current_job_status = self.status

    def wait_for_completion(self, timeout=30, **kwargs):
        """Waits till the job is not finished; i.e.; till the value of job.is_finished is not True.
            Kills the job and exits, if the job has been in Pending / Waiting state for more than
            the timeout value.

            In case of job failure job status and failure reason can be obtained
                using status and delay_reason property

            Args:
                timeout     (int)   --  minutes after which the job should be killed and exited,
                        if the job has been in Pending / Waiting state
                    default: 30

                **kwargs    (str)   --  accepted optional arguments

                    return_timeout  (int)   -- minutes after which the method will return False.

            Returns:
                bool    -   boolean specifying whether the job had finished or not
                    True    -   if the job had finished successfully

                    False   -   if the job was killed/failed

        """
        start_time = actual_start_time = time.time()
        pending_time = 0
        waiting_time = 0
        previous_status = None
        return_timeout = kwargs.get('return_timeout')

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
                break

            # set the value of previous status as the value of current status
            previous_status = status
        else:
            return self._status.lower() not in ["failed", "killed", "failed to start"]

        return False

    @property
    def is_finished(self):
        """Checks whether the job has finished or not.

            Returns:
                bool    -   boolean that represents whether the job has finished or not

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
    def client_name(self):
        """Treats the client name as a read-only attribute."""
        if 'clientName' in self._summary['subclient']:
            return self._summary['subclient']['clientName']

    @property
    def agent_name(self):
        """Treats the agent name as a read-only attribute."""
        if 'appName' in self._summary['subclient']:
            return self._summary['subclient']['appName']

    @property
    def instance_name(self):
        """Treats the instance name as a read-only attribute."""
        if 'instanceName' in self._summary['subclient']:
            return self._summary['subclient']['instanceName']

    @property
    def backupset_name(self):
        """Treats the backupset name as a read-only attribute."""
        if 'backupsetName' in self._summary['subclient']:
            return self._summary['subclient']['backupsetName']

    @property
    def subclient_name(self):
        """Treats the subclient name as a read-only attribute."""
        if 'subclientName' in self._summary['subclient']:
            return self._summary['subclient']['subclientName']

    @property
    def status(self):
        """Treats the job status as a read-only attribute.
           http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm
           please refer status section in above doc link for complete list of status available"""
        self.is_finished
        return self._status

    @property
    def job_id(self):
        """Treats the job id as a read-only attribute."""
        return self._job_id

    @property
    def job_type(self):
        """Treats the job type as a read-only attribute."""
        return self._summary['jobType']

    @property
    def backup_level(self):
        """Treats the backup level as a read-only attribute."""
        if 'backupLevelName' in self._summary:
            return self._summary['backupLevelName']

    @property
    def start_time(self):
        """Treats the start time as a read-only attribute."""
        return self._start_time
    
    @property
    def start_timestamp(self):
        """Treats the unix start time as a read-only attribute."""
        return self._summary['jobStartTime']

    @property
    def end_timestamp(self):
        """Treats the unix end time as a read-only attribute"""
        return self._summary['jobEndTime']

    @property
    def end_time(self):
        """Treats the end time as a read-only attribute."""
        return self._end_time

    @property
    def delay_reason(self):
        """Treats the job delay reason as a read-only attribute."""
        self.is_finished
        progress_info = self._details['jobDetail']['progressInfo']
        if 'reasonForJobDelay' in progress_info and progress_info['reasonForJobDelay']:
            return progress_info['reasonForJobDelay']

    @property
    def pending_reason(self):
        """Treats the job pending reason as a read-only attribute."""
        self.is_finished
        if 'pendingReason' in self._summary and self._summary['pendingReason']:
            return self._summary['pendingReason']

    @property
    def phase(self):
        """Treats the job current phase as a read-only attribute."""
        self.is_finished
        if 'currentPhaseName' in self._summary:
            return self._summary['currentPhaseName']

    @property
    def attempts(self):
        """Returns job attempts data as read-only attribute"""
        self.is_finished
        return self._details.get('jobDetail', {}).get('attemptsInfo', {})

    @property
    def summary(self):
        """Treats the job full summary as a read-only attribute."""
        self.is_finished
        return self._summary

    @property
    def username(self):
        """Treats the username as a read-only attribute."""
        return self._summary['userName']['userName']

    @property
    def userid(self):
        """Treats the userid as a read-only attribute."""
        return self._summary['userName']['userId']

    @property
    def details(self):
        """Treats the job full details as a read-only attribute."""
        self.is_finished
        return self._details

    @property
    def size_of_application(self):
        """Treats the size of application as a read-only attribute."""
        if 'sizeOfApplication' in self._summary:
            return self._summary['sizeOfApplication']

    @property
    def media_size(self):
        """
        Treats the size of media as a read-only attribute
        Returns:
            integer - size of media or data written
        """
        return self._summary.get('sizeOfMediaOnDisk', 0)

    @property
    def num_of_files_transferred(self):
        """Treats the number of files transferred as a read-only attribute."""
        self.is_finished
        return self._details['jobDetail']['progressInfo']['numOfFilesTransferred']

    @property
    def state(self):
        """Treats the job state as a read-only attribute."""
        self.is_finished
        return self._details['jobDetail']['progressInfo']['state']

    @property
    def task_details(self):
        """Returns: (dict) A dictionary of job task details"""
        if not self._task_details:
            self._task_details = self._get_job_task_details()
        return self._task_details

    def pause(self, wait_for_job_to_pause=False, timeout=6):
        """Suspends the job.

            Args:
                wait_for_job_to_pause   (bool)  --  wait till job status is changed to Suspended

                    default: False

                timeout (int)                   --  timeout interval to wait for job to move to suspend state

            Raises:
                SDKException:
                    if failed to suspend job

                    if response is not success

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

    def resume(self, wait_for_job_to_resume=False):
        """Resumes the job.

            Args:
                wait_for_job_to_resume  (bool)  --  wait till job status is changed to Running

                    default: False

            Raises:
                SDKException:
                    if failed to resume job

                    if response is not success

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

    def resubmit(self, start_suspended=None):
        """Resubmits the job

        Args:
            start_suspended (bool)  -   whether to start the new job in suspended state or not
                                        default: None, the new job starts same as this job started

        Returns:
            object  -   Job class object for the given job id

        Raises:
                SDKException:
                    if job is already running

                    if response is not success

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

    def kill(self, wait_for_job_to_kill=False):
        """Kills the job.

            Args:
                wait_for_job_to_kill    (bool)  --  wait till job status is changed to Killed

                    default: False

            Raises:
                SDKException:
                    if failed to kill job

                    if response is not success

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

    def refresh(self):
        """Refresh the properties of the Job."""
        self._initialize_job_properties()
        self.is_finished

    def advanced_job_details(self, info_type):
        """Returns advanced properties for the job

            Args:
                infoType    (object)  --  job detail type to be passed from AdvancedJobDetailType
                enum from the constants

            Returns:
                dict -  dictionary with advanced details of the job info type given

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def get_events(self):
        """ gets the commserv events associated with this job

            Args:

                None

            Returns:

                list - list of job events

                    Example : [
                        {
                            "severity": 3,
                            "eventCode": "318769020",
                            "jobId": 4547,
                            "acknowledge": 0,
                            "eventCodeString": "19:1916",
                            "subsystem": "JobManager",
                            "description": "Data Analytics operation has completed with one or more errors.",
                            "id": 25245,
                            "timeSource": 1600919001,
                            "type": 0,
                            "clientEntity": {
                                "clientId": 2,
                                "clientName": "xyz",
                                "displayName": "xyz"
                            }
                        },
                        {
                            "severity": 6,
                            "eventCode": "318767961",
                            "jobId": 4547,
                            "acknowledge": 0,
                            "eventCodeString": "19:857",
                            "subsystem": "clBackup",
                            "description": "Failed to send some items to Index Engine",
                            "id": 25244,
                            "timeSource": 1600918999,
                            "type": 0,
                            "clientEntity": {
                                "clientId": 33,
                                "clientName": "xyz",
                                "displayName": "xyz"
                            }
                        }
                    ]

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._JOB_EVENTS)
        if flag:
            if response.json() and 'commservEvents' in response.json():
                    return response.json()['commservEvents']
            raise SDKException('Job', '104')
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_vm_list(self):
        """
        Gets the list of all VMs associated to the job
        Returns: list of VM dictionaries
            VM: {
               "Size":0,
               "AverageThroughput":0,
               "UsedSpace":0,
               "ArchivedByCurrentJob":false,
               "jobID":0,
               "CBTStatus":"",
               "BackupType":0,
               "totalFiles":0,
               "Status":2,
               "CurrentThroughput":0,
               "Agent":"proxy",
               "lastSyncedBkpJob":0,
               "GUID":"live sync pair guid",
               "HardwareVersion":"vm h/w",
               "restoredSize":1361912,
               "FailureReason":"",
               "BackupStartTime":0,
               "TransportMode":"nbd",
               "projectId":"",
               "syncStatus":3,
               "PoweredOffSince":0,
               "OperatingSystem":"Microsoft Windows Server 2012 (64-bit)",
               "backupLevel":0,
               "destinationVMName":"drvm1",
               "successfulCIedFiles":0,
               "GuestSize":0,
               "failedCIedFiles":0,
               "vmName":"vm1",
               "ToolsVersion":"Not running",
               "clientId":3280,
               "Host":"1.1.1.1",
               "StubStatus":0,
               "BackupEndTime":0,
               "PoweredOffByCurrentJob":false
            }
        """
        return self.details.get('jobDetail', {}).get('clientStatusInfo', {}).get('vmStatus', [])

    def get_child_jobs(self):
        """ Get the child jobs details for the current job
        Returns:
                _jobs_list          (list):     List of child jobs

        """
        _jobs_list = []
        if self.details.get('jobDetail', {}).get('clientStatusInfo', {}).get('vmStatus'):
            for _job in self.details['jobDetail']['clientStatusInfo']['vmStatus']:
                _jobs_list.append(_job)
            return _jobs_list
        else:
            return None


class _ErrorRule:
    """Class for enabling, disabling, adding, getting and deleting error rules."""

    def __init__(self, commcell):
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

    def _get_xml_for_rule(self, rule_dict):
        """
        Returns the XML for a given rule's dictionary of key value pairs. The XML output is used internally when
        when adding new or updating existing rules.

        Args:
            rule_dict   (dict)  -   Dictionary of a rule's key value pairs.

        Returns:
            str -   The XML output formatted as a string.

        Raises:
            None

        """

        return self.error_rule_str.format(
            pattern=rule_dict['pattern'],
            all_error_codes=rule_dict['all_error_codes'],
            from_error_code=rule_dict['from_error_code'],
            to_error_code=rule_dict['to_error_code'],
            job_decision=rule_dict['job_decision'],
            is_enabled=rule_dict['is_enabled'],
            skip_reporting_error=rule_dict['skip_reporting_error'])

    def add_error_rule(self, rules_arg):
        """
        Add new error rules as well as update existing rules, each rule is identified by its rule name denoted by key
        rule_name.

            Args:
                rules_arg   (dict)  --  A dictionary whose key is the application group name and value is a rules list.

                    Supported value(s) for key is all constants under ApplicationGroup(Enum)

                    The value for above key is a list
                    where each item of the list is a dictionary of the following key value pairs.

                        is_enabled              (str)   --  Specifies whether the rule should be enabled or not.

                        pattern                 (str)   --  Specifies the file pattern for the error rule.

                        all_error_codes         (bool)  --  Specifies whether all error codes should be enabled.

                        from_error_code         (int)   --  Error code range's lower value.
                        Valid values are all non negative integers.

                        to_error_code           (int)   --  Error code range's upper value.
                        Valid values are all non negative integers higher larger the from_ec value.

                        skip_reporting_error    (bool)  --  Specifies if error codes need to be skipped from being reported.

                    Example:
                            {
                             WINDOWS : { 'rule_1': { 'appGroupName': WINDOWS,
                                                     'pattern': "*",
                                                     'all_error_codes': False,
                                                     'from_error_code': 1,
                                                     'to_error_code': 2,
                                                     'job_decision': 0,
                                                     'is_enabled': True,
                                                     'skip_reporting_error': False
                                                   },
                                         'rule_2' : { ......}
                                       }
                            }

            Returns:
                None

            Raises:
                Exception in case of invalid key/value pair(s).
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

    def enable(self, app_group):
        """Enables the job error control rules for the specified Application Group Type.
            Args:
                app_group   (str)   --  The iDA for which the enable flag needs to be set.
                Currently supported values are APPGRP_WindowsFileSystemIDA.

            Returns:
                None

            Raises:
                None

        """
        return self._modify_job_status_on_errors(app_group, enable_flag=True)

    def disable(self, app_group):
        """Disables the job error control rules for the specified Application Group Type.
            Args:
                app_group   (str)   --  The iDA for which the enable flag needs to be set.
                Currently supported values are APPGRP_WindowsFileSystemIDA.

            Returns:
                None

            Raises:
                None
        """
        return self._modify_job_status_on_errors(app_group, enable_flag=False)

    def _modify_job_status_on_errors(self, app_group, enable_flag):
        """To enable or disable job status on errors.
            Args:
                app_group   (str)   --  The iDA for which the enable flag needs to be set.
                Currently supported values are APPGRP_WindowsFileSystemIDA.

                enable_flag (bool)  --  Enables and disables job status on errors.
            Returns:
                None

            Raises:
                None
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

    def _get_error_rules(self, app_group):
        """
        Returns the error rules set on the CS in the form of a dictionary.

        Args:
            app_group   (str)   --  The iDA for which the enable flag needs to be set.
                Currently supported values are APPGRP_WindowsFileSystemIDA.

        Returns:
            list    -   A list of error rules. Each rule will be a dictionary of key value pairs for pattern,
            error code from value, error code to value etc.

        Raises:
            None
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
