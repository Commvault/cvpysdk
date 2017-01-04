#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on a job.

Job: Class for keeping track of a job and perform various operations on it.

Job:
    __init__(commcell_object,
             job_id)            --  initialises the instance of Job class associated with the
                                        specified commcell of job with id: 'job_id'
    __repr__()                  --  returns the string representation of the object of this class,
                                        with the job id it is associated with
    _is_valid_job()             --  checks if the job with the given id is a valid job or not.
    _check_finished()           --  checks if the job has finished or not yet
    _is_finished()              --  checks for the status of the job.
                                        Returns True if finished, else False
    get_job_summary()           --  gets the summary of the job with the given job id
    get_job_details()           --  gets the details of the job with the given job id
    pause()                     --  suspend the job
    resume()                    --  resumes the job
    kill()                      --  kills the job


job.status                      --  Gives the current status of the job.
                                        (Completed / Suspended / Waiting / ... / etc.)
job.finished                    --  Tells whether the job is finished or not. (True / False)

"""

import time
import threading

from exception import SDKException


class Job(object):
    """Class for performing client operations for a specific client."""

    def __init__(self, commcell_object, job_id):
        """Initialise the Job class instance.

            Args:
                commcell_object (object)  --  instance of the Commcell class
                job_id (str / int)        --  id of the job

            Returns:
                object - instance of the Job class

            Raises:
                SDKException:
                    if job id is not of type int
                    if job is not a valid job, i.e., does not exist in the Commcell
        """
        try:
            int(job_id)
        except ValueError:
            raise SDKException('Job', '101')

        self._commcell_object = commcell_object
        self._job_id = str(job_id)

        self._JOB = self._commcell_object._services.JOB % (self.job_id)
        if not self._is_valid_job():
            raise SDKException('Job', '102')

        self._JOB_DETAILS = self._commcell_object._services.JOB_DETAILS
        self._SUSPEND = self._commcell_object._services.SUSPEND_JOB % (self.job_id)
        self._RESUME = self._commcell_object._services.RESUME_JOB % (self.job_id)
        self._KILL = self._commcell_object._services.KILL_JOB % (self.job_id)

        self.finished = self._is_finished()
        self.status = str(self.get_job_summary()['status'])

        self._initialize_job_properties()

        thread = threading.Thread(target=self._check_finished)
        thread.start()

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
        if self.get_job_summary() is False:
            return False
        else:
            return True

    def _check_finished(self):
        """Checks whether the job has finished or not.

            Returns:
                None
        """
        while not self._is_finished():
            time.sleep(5)
        self.finished = self._is_finished()

    def _is_finished(self):
        """Checks whether the job has finished or not.

            Returns:
                bool - boolean that represents whether the job has finished or not
        """
        self.status = str(self.get_job_summary()['status'])

        return ('completed' in self.status.lower() or
                'killed' in self.status.lower() or
                'failed' in self.status.lower())

    def _initialize_job_properties(self):
        """Initializes the common properties for the job.
            Adds the client, agent, backupset, subclient name to the job object.

            Returns:
                None
        """
        subclient_properties = self.get_job_summary()['subclient']
        self._client_name = str(subclient_properties['clientName'])
        self._agent_name = str(subclient_properties['appName'])
        self._backupset_name = str(subclient_properties['backupsetName'])

        if 'subclientName' in subclient_properties:
            self._subclient_name = str(subclient_properties['subclientName'])
        else:
            self._subclient_name = 'Not provided in Job details'

    @property
    def client_name(self):
        """Treats the client name as a read-only attribute."""
        return self._client_name

    @property
    def agent_name(self):
        """Treats the agent name as a read-only attribute."""
        return self._agent_name

    @property
    def backupset_name(self):
        """Treats the backupset name as a read-only attribute."""
        return self._backupset_name

    @property
    def subclient_name(self):
        """Treats the subclient name as a read-only attribute."""
        return self._subclient_name

    @property
    def job_id(self):
        """Treats the job id as a read-only attribute."""
        return self._job_id

    def get_job_summary(self):
        """Gets the properties of this job.

            Returns:
                dict - dict that contains the summary of this job

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._JOB)

        if flag:
            if response.json():
                if response.json()['totalRecordsWithoutPaging'] == 0:
                    return False
                if 'jobs' in response.json().keys():
                    for job in response.json()['jobs']:
                        return job['jobSummary']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_job_details(self):
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
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            self._JOB_DETAILS,
                                                                            payload)

        if flag:
            if response.json() and 'job' in response.json().keys():
                return response.json()['job']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def pause(self):
        """Suspend the job.

            Returns:
                None

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._SUSPEND)

        if flag:
            if response.json() and 'errors' in response.json():
                error_list = response.json()['errors'][0]['errList'][0]
                error_message = str(error_list['errLogMessage']).strip()
                error_code = str(error_list['errorCode']).strip()

                print 'Job suspend failed with error message: "%s", and error code: "%s"' % \
                    (error_message, error_code)
            else:
                self.status = str(self.get_job_summary()['status'])
                print 'Job suspended successfully'
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def resume(self):
        """Resume the job.

            Returns:
                None

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._RESUME)

        if flag:
            if response.json() and 'errors' in response.json():
                error_list = response.json()['errors'][0]['errList'][0]
                error_message = str(error_list['errLogMessage']).strip()
                error_code = str(error_list['errorCode']).strip()

                print 'Job resume failed with error message: "%s", and error code: "%s"' % \
                    (error_message, error_code)
            else:
                self.status = str(self.get_job_summary()['status'])
                print 'Job resumed successfully'
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def kill(self):
        """Kill the job.

            Returns:
                None

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._KILL)

        if flag:
            if response.json() and 'errors' in response.json():
                error_list = response.json()['errors'][0]['errList'][0]
                error_message = str(error_list['errLogMessage']).strip()
                error_code = str(error_list['errorCode']).strip()

                print 'Job kill failed with error message: "%s", and error code: "%s"' % \
                    (error_message, error_code)
            else:
                self.status = str(self.get_job_summary()['status'])
                self.finished = True
                print 'Job killed successfully'
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
