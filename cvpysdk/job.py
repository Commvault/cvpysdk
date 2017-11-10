#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on a job.

JobController:  Class for managing jobs on this commcell

Job: Class for keeping track of a job and perform various operations on it.


JobController:
    __init__(commcell_object)   --  initializes the instance of JobController class associated
                                        with the specified commcell

    __str__()                   --  returns the string representation of the active jobs
                                        on this commcell

    __repr__()                  --  returns the string representation of the object of this class,
                                        with the commcell it is associated with

    _all_jobs_request_json()    --  returns the request json to get list of all jobs on commcell

    all_jobs()                  --  returns all the jobs on this commcell

    active_jobs()               --  returns the dict of active jobs and their details

    finished_jobs()             --  retutns the dict of finished jobs and their details

    get()                       --  returns the Job class object for the specified job id


Job:
    __init__(commcell_object,
             job_id)            --  initializes the instance of Job class associated with the
                                        specified commcell of job with id: 'job_id'

    __repr__()                  --  returns the string representation of the object of this class,
                                        with the job id it is associated with

    _is_valid_job()             --  checks if the job with the given id is a valid job or not.

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

Usage:

job.status                      --  Gives the current status of the job.
                                        (Completed / Suspended / Waiting / ... / etc.)

job.is_finished                 --  Tells whether the job is finished or not. (True / False)

job.pending_reason              --  reason if job went into pending state

job.delay_reason                --  reason why the job was delayed

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import time

from .exception import SDKException


class JobController(object):
    """Class for controlling all the jobs associated with the commcell."""

    def __init__(self, commcell_object):
        self._commcell_object = commcell_object
        self._ALl_JOBS = self._commcell_object._services['ALL_JOBS']

    def __str__(self):
        """Representation string consisting of all active jobs on this commcell.

            Returns:
                str - string of all the active jobs on this commcell
        """
        jobs_dict = self.active_jobs()
        representation_string = '{:^5}\t{:^25}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'Job ID', 'Operation', 'Status', 'Agent type', 'Job type',
            'Progress', 'Pending Reason'
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
            self._commcell_object._headers['Host']
        )

    def _all_jobs_request_json(self, category='ALL', limit=20, lookup_time=5):
        """Returns the request json for the jobs request

            Args:
                category    (str)   --  category name for which the list of jobs
                                            are to be retrieved
                        default: ALL
                    Accept: ALL/ ACTIVE/ FINISHED

                limit       (int)   --  total number of jobs list that are to be returned
                        default: 20

                lookup_time (int)   --  list of jobs to be retrieved which are specified
                                            minutes older
                        default: 5 minutes

            Returns:
                dict    -   request json that is to be sent to server
        """
        job_list_category = {
            'ALL': 0,
            'ACTIVE': 1,
            'FINISHED': 2
        }

        request_json = {
            "scope": 1,
            "category": job_list_category[category],
            "pagingConfig": {
                "sortDirection": 1,
                "offset": 0,
                "sortField": "jobId",
                "limit": limit
            },
            "jobFilter": {
                "completedJobLookupTime": lookup_time * 60,
                "showAgedJobs": False
            }
        }

        return request_json

    def _get_jobs_list(self, request_json):
        """Makes the GET request to server to get list of jobs

            Args:
                request_json    (dict)  --  request that is to be sent to server

            Returns:
                dict    -   dict containing details about all the retrieved jobs

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._ALl_JOBS, request_json
        )

        jobs_dict = {}

        if flag:
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

                            if 'appTypeName' in job_summary:
                                app_type = job_summary['appTypeName']

                            if 'jobType' in job_summary:
                                job_type = job_summary['jobType']

                            if 'pendingReason' in job_summary:
                                pending_reason = job_summary['pendingReason']

                            jobs_dict[job_id] = {
                                'operation': operation,
                                'status': status,
                                'app_type': app_type,
                                'job_type': job_type,
                                'percent_complete': percent_complete,
                                'pending_reason': pending_reason
                            }

                return jobs_dict

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def all_jobs(self, limit=20, lookup_time=1440):
        """Returns the dict containing all the jobs on this commcell
            which are specified time older

            Args:
                limit       (int)   --  total number of jobs list that are to be returned
                        default: 20

                lookup_time (int)   --  list of jobs to be retrieved which are specified
                                            minutes older
                        default: 1440 minutes

            Returns:
                dict    -   request json that is to be sent to server
        """
        request_json = self._all_jobs_request_json(
            category='ALL', limit=limit, lookup_time=lookup_time
        )

        return self._get_jobs_list(request_json)

    def active_jobs(self, limit=20, lookup_time=5):
        """Returns the dict containing all the active jobs on this commcell
            which are specified time older

            Args:
                limit       (int)   --  total number of jobs list that are to be returned
                        default: 20

                lookup_time (int)   --  list of jobs to be retrieved which are specified
                                            minutes older
                        default: 5 minutes

            Returns:
                dict    -   request json that is to be sent to server
        """
        request_json = self._all_jobs_request_json(
            category='ACTIVE', limit=limit, lookup_time=lookup_time
        )

        return self._get_jobs_list(request_json)

    def finished_jobs(self, limit=20, lookup_time=1440):
        """Returns the dict containing all the finished jobs on this commcell
            which are specified time older

            Args:
                limit       (int)   --  total number of jobs list that are to be returned
                        default: 20

                lookup_time (int)   --  list of jobs to be retrieved which are specified
                                            minutes older
                        default: 1440 minutes

            Returns:
                dict    -   request json that is to be sent to server
        """
        request_json = self._all_jobs_request_json(
            category='FINISHED', limit=limit, lookup_time=lookup_time
        )

        return self._get_jobs_list(request_json)

    def get(self, job_id):
        """Returns the job object for the soecified job id

            Args:
                job_id      (int)   --  id of the job for which the Job class object
                                            is to be created

            Returns:
                object  -   Job class object for the specified job id

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
                commcell_object (object)     --  instance of the Commcell class

                job_id          (str / int)  --  id of the job

            Returns:
                object - instance of the Job class

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
        self._job_id = str(job_id)

        self._JOB = self._commcell_object._services['JOB'] % (self.job_id)

        if not self._is_valid_job():
            raise SDKException('Job', '103')

        self._JOB_DETAILS = self._commcell_object._services['JOB_DETAILS']
        self._SUSPEND = self._commcell_object._services['SUSPEND_JOB'] % (self.job_id)
        self._RESUME = self._commcell_object._services['RESUME_JOB'] % (self.job_id)
        self._KILL = self._commcell_object._services['KILL_JOB'] % (self.job_id)

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

        self._initialize_job_properties()
        self.is_finished

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string for instance of this class
        """
        representation_string = 'Job class instance for job id: "{0}"'
        return representation_string.format(self.job_id)

    def _is_valid_job(self):
        """Checks if the job submitted with the job id is a valid job or not.

            Returns:
                bool - boolean that represents whether the job is valid or not
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
                dict - dict that contains the summary of this job

            Raises:
                SDKException:
                    if no record found for this job

                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._JOB)

        if flag:
            if response.json():
                if response.json()['totalRecordsWithoutPaging'] == 0:
                    raise SDKException('Job', '104')

                if 'jobs' in response.json():
                    for job in response.json()['jobs']:
                        return job['jobSummary']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_job_details(self):
        """Gets the detailed properties of this job.

            Returns:
                dict - dict consisting of the detailed properties of the job

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        payload = {
            "jobId": int(self.job_id)
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._JOB_DETAILS, payload
        )

        if flag:
            if response.json() and 'job' in response.json():
                return response.json()['job']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_job_properties(self):
        """Initializes the common properties for the job.
            Adds the client, agent, backupset, subclient name to the job object.
        """
        job_summary = self._get_job_summary()
        job_details = self._get_job_details()

        subclient_properties = job_summary['subclient']

        if 'clientName' in subclient_properties:
            self._client_name = subclient_properties['clientName']

        if 'appName' in subclient_properties:
            self._agent_name = subclient_properties['appName']

        if 'instanceName' in subclient_properties:
            self._instance_name = subclient_properties['instanceName']

        if 'backupsetName' in subclient_properties:
            self._backupset_name = subclient_properties['backupsetName']

        if 'subclientName' in subclient_properties:
            self._subclient_name = subclient_properties['subclientName']

        self._status = job_summary['status']

        self._job_type = job_summary['jobType']

        if self._job_type == 'Backup' and 'backupLevelName' in job_summary:
            self._backup_level = job_summary['backupLevelName']

        self._start_time = time.ctime(job_summary['jobStartTime'])

        if 'pendingReason' in job_summary:
            if job_summary['pendingReason']:
                self._pending_reason = job_summary['pendingReason']

        if 'reasonForJobDelay' in job_details['jobDetail']['progressInfo']:
            if job_details['jobDetail']['progressInfo']['reasonForJobDelay']:
                self._delay_reason = job_details['jobDetail']['progressInfo']['reasonForJobDelay']

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
                bool - boolean that represents whether the job has finished or not
        """
        job_summary = self._get_job_summary()
        job_details = self._get_job_details()

        self._status = job_summary['status']

        if job_summary['lastUpdateTime'] != 0:
            self._end_time = time.ctime(job_summary['lastUpdateTime'])

        if 'pendingReason' in job_summary:
            if job_summary['pendingReason']:
                self._pending_reason = job_summary['pendingReason']

        if 'reasonForJobDelay' in job_details['jobDetail']['progressInfo']:
            if job_details['jobDetail']['progressInfo']['reasonForJobDelay']:
                self._delay_reason = job_details['jobDetail']['progressInfo']['reasonForJobDelay']

        return ('completed' in self._status.lower() or
                'killed' in self._status.lower() or
                'failed' in self._status.lower())

    @property
    def client_name(self):
        """Treats the client name as a read-only attribute."""
        return self._client_name

    @property
    def agent_name(self):
        """Treats the agent name as a read-only attribute."""
        return self._agent_name

    @property
    def instance_name(self):
        """Treats the instance name as a read-only attribute."""
        return self._instance_name

    @property
    def backupset_name(self):
        """Treats the backupset name as a read-only attribute."""
        return self._backupset_name

    @property
    def subclient_name(self):
        """Treats the subclient name as a read-only attribute."""
        return self._subclient_name

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
        return self._job_type

    @property
    def backup_level(self):
        """Treats the backup level as a read-only attribute."""
        return self._backup_level

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
        return self._delay_reason

    @property
    def pending_reason(self):
        """Treats the job pending reason as a read-only attribute."""
        self.is_finished
        return self._pending_reason

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._SUSPEND)

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
            response_string = self._commcell_object._update_response_(response.text)
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
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._RESUME)

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
            response_string = self._commcell_object._update_response_(response.text)
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
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._KILL)

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if wait_for_job_to_kill is True:
            self._wait_for_status("KILLED")
