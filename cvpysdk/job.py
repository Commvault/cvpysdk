# -*- coding: utf-8 -*-
# pylint: disable=W0104, R0205, R1710

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on a job.

JobController:  Class for managing jobs on this commcell

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

    _wait_for_status()          --  waits for 2 minutes or till the job status is changed
    to given status, whichever is earlier

    wait_for_completion()       --  waits for the job to finish, (job.is_finished == True)

    is_finished()               --  checks for the status of the job.

                                        Returns True if finished, else False

    pause()                     --  suspend the job

    resume()                    --  resumes the job

    kill()                      --  kills the job

    refresh()                   --  refresh the properties of the Job

    advanced_job_details()      --  Returns advanced properties for the job


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


**job.job_id**                      --  returns the id of the job

**job.job_type**                    --  returns the type of the job

**job.backup_level**                --  returns the backup level (if applicable), otherwise None

**job.start_time**                  --  returns the start time of the job

**job.end_time**                    --  returns the end time of the job

**job.delay_reason**                --  reason why the job was delayed

**job.pending_reason**              --  reason if job went into pending state

**job.phase**                       --  returns the current phase of the job

**job.summary**                     --  returns the dictionary consisting of the full summary of the job

**job.details**                     --  returns the dictionary consisting of the full details of the job

**job.num_of_files_transferred**    -- returns the current number of files transferred for the job.

**job.state**                       -- returns the current state of the job.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import time

from .exception import SDKException
from .constants import AdvancedJobDetailType


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
        return "JobController class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

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

                    lookup_time     (int)   --  list of jobs to be retrieved which are specified
                    hours older

                            default: 5 hours

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                            default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                            default: []

                    job_type_list   (list)  --  list of job operation types

                            default: []

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

        request_json = {
            "scope": 1,
            "category": job_list_category[options.get('category', 'ALL')],
            "pagingConfig": {
                "sortDirection": 1,
                "offset": 0,
                "sortField": "jobId",
                "limit": options.get('limit', 20)
            },
            "jobFilter": {
                "completedJobLookupTime": int(options.get('lookup_time', 5) * 60 * 60),
                "showAgedJobs": options.get('show_aged_jobs', False),
                "clientList": [
                    {
                        "clientId": int(self._commcell_object.clients.all_clients[client]['id'])
                    } for client in options.get('clients_list', [])
                ],
                "jobTypeList": [
                    job_type for job_type in options.get('job_type_list', [])
                ]
            }
        }

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

                                status = job_summary['status']
                                operation = job_summary['localizedOperationName']
                                percent_complete = job_summary['percentComplete']

                                app_type = ''
                                job_type = ''
                                pending_reason = ''
                                subclient_id = ''

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

                                jobs_dict[job_id] = {
                                    'operation': operation,
                                    'status': status,
                                    'app_type': app_type,
                                    'job_type': job_type,
                                    'percent_complete': percent_complete,
                                    'pending_reason': pending_reason,
                                    'subclient_id': subclient_id
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

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                        default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                        default: []

                    job_type_list   (list)  --  list of job operation types

                        default: []

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

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                        default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                        default: []

                    job_type_list   (list)  --  list of job operation types

                        default: []


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

                    show_aged_job   (bool)  --  boolean specifying whether to include aged jobs in
                    the result or not

                        default: False

                    clients_list    (list)  --  list of clients to return the jobs for

                        default: []

                    job_type_list   (list)  --  list of job operation types

                        default: []


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
            raise SDKException('Job', '103')

        self._JOB_DETAILS = self._services['JOB_DETAILS']
        self.ADVANCED_JOB_DETAILS = AdvancedJobDetailType
        self._SUSPEND = self._services['SUSPEND_JOB'] % (self.job_id)
        self._RESUME = self._services['RESUME_JOB'] % (self.job_id)
        self._KILL = self._services['KILL_JOB'] % (self.job_id)

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
        flag, response = self._cvpysdk_object.make_request('GET', self._JOB)

        if flag:
            if response.json():
                if response.json().get('totalRecordsWithoutPaging', 0) == 0:
                    raise SDKException('Job', '104')

                if 'jobs' in response.json():
                    for job in response.json()['jobs']:
                        return job['jobSummary']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
            "jobId": int(self.job_id)
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._JOB_DETAILS, payload)

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
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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

    def _wait_for_status(self, status):
        """Waits for 2 minutes or till the job status is changed to given status,
            whichever is earlier.

            Args:
                status  (str)   --  Job Status

            Returns:
                None

        """
        start_time = time.time()

        while self.status.lower() != status.lower():
            if (self.is_finished is True) or (time.time() - start_time > 120):
                break

            time.sleep(3)

    def wait_for_completion(self, timeout=30):
        """Waits till the job is not finished; i.e.; till the value of job.is_finished is not True.
            Kills the job and exits, if the job has been in Pending / Waiting state for more than
            the timeout value.

            In case of job failure job status and failure reason can be obtained
                using status and delay_reason property

            Args:
                timeout     (int)   --  minutes after which the job should be killed and exited,
                        if the job has been in Pending / Waiting state
                    default: 30

            Returns:
                bool    -   boolean specifying whether the job had finished or not
                    True    -   if the job had finished successfully

                    False   -   if the job was killed/failed

        """
        start_time = time.time()
        pending_time = 0
        waiting_time = 0
        previous_status = None

        status_list = ['pending', 'waiting']

        while not self.is_finished:
            time.sleep(30)

            # get the current status of the job
            status = self.status.lower()

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
            return self._status.lower() not in ["failed", "killed"]

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
        """Treats the job status as a read-only attribute."""
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
    def summary(self):
        """Treats the job full summary as a read-only attribute."""
        self.is_finished
        return self._summary

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
    def num_of_files_transferred(self):
        """Treats the number of files transferred as a read-only attribute."""
        self.is_finished
        return self._details['jobDetail']['progressInfo']['numOfFilesTransferred']

    @property
    def state(self):
        """Treats the job state as a read-only attribute."""
        self.is_finished
        return self._details['jobDetail']['progressInfo']['state']

    def pause(self, wait_for_job_to_pause=False):
        """Suspends the job.

            Args:
                wait_for_job_to_pause   (bool)  --  wait till job status is changed to Suspended

                    default: False

            Raises:
                SDKException:
                    if failed to suspend job

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('POST', self._SUSPEND)

        self.is_finished

        if flag:
            if response.json() and 'errors' in response.json():
                error_list = response.json()['errors'][0]['errList'][0]
                error_code = error_list['errorCode']
                error_message = error_list['errLogMessage'].strip()

                if error_code != 0:
                    raise SDKException(
                        'Job', '102', 'Job suspend failed\nError: "{0}"'.format(error_message)
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if wait_for_job_to_pause is True:
            self._wait_for_status("SUSPENDED")

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
            if response.json() and 'errors' in response.json():
                error_list = response.json()['errors'][0]['errList'][0]
                error_code = error_list['errorCode']
                error_message = error_list['errLogMessage'].strip()

                if error_code != 0:
                    raise SDKException(
                        'Job', '102', 'Job resume failed\nError: "{0}"'.format(error_message)
                    )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if wait_for_job_to_resume is True:
            self._wait_for_status("RUNNING")

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
            if response.json() and 'errors' in response.json():
                error_list = response.json()['errors'][0]['errList'][0]
                error_code = error_list['errorCode']
                error_message = error_list['errLogMessage'].strip()

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
