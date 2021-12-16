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

"""Main file for performing operations on ediscovery clients.

'EdiscoveryClientOperations' is the only class defined in this file

EdiscoveryClientOperations : Class for performing operations on Ediscovery clients

EdiscoveryClientOperations:

    __init__()                          --  initialise object of the EdiscoveryClientOperations class

    _response_not_success()             --  parses through the exception response, and raises SDKException

    start_job()                         --  starts collection job on ediscovery client

    get_job_status()                    --  returns the job status of ediscovery client job

    get_job_history()                   --  returns the job history details of this ediscovery client

    wait_for_collection_job()           --  waits for collection job to finish

"""
import time

from ..activateapps.constants import InventoryConstants
from ..exception import SDKException


class EdiscoveryClientOperations():
    """Class for performing operations on ediscovery clients."""

    def __init__(self, commcell_object, class_object):
        """Initializes an instance of the EdiscoveryClientOperations class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                class_object        (object)    -- instance of Inventory/Asset class

            Returns:
                object  -   instance of the EdiscoveryClientOperations class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._class_obj = class_object
        self._type = None
        self._operation = None
        self._client_id = None
        self._data_source_id = None
        self._API_CRAWL = self._services['EDISCOVERY_CRAWL']
        self._API_JOBS_HISTORY = self._services['EDISCOVERY_JOBS_HISTORY']
        self._API_JOB_STATUS = self._services['EDISCOVERY_JOB_STATUS']

        from .inventory_manager import Inventory, Asset

        if isinstance(class_object, Inventory):
            self._type = 0
            self._operation = 0
            self._client_id = class_object.inventory_id
            self._data_source_id = 0
        elif isinstance(class_object, Asset):
            self._type = 0
            self._operation = 0
            self._client_id = class_object.inventory_id
            self._data_source_id = class_object.asset_id
        else:
            raise SDKException('EdiscoveryClients', '101')

    def start_job(self, wait_for_job=False, wait_time=60):
        """Starts job on ediscovery client

            Args:

                    wait_for_job        (bool)       --  specifies whether to wait for job to complete or not

                    wait_time           (int)        --  time interval to wait for job completion in Mins
                                                            Default : 60Mins

             Return:

                    None

            Raises:

                    SDKException:

                            if failed to start collection job

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_CRAWL % (self._client_id, self._data_source_id, self._type, self._operation)
        )
        if flag:
            if response.json():
                response_json = response.json()
                if 'errorCode' in response_json:
                    error_code = response_json['errorCode']
                    if error_code != 0:
                        error_message = response_json['errorMessage']
                        raise SDKException(
                            'EdiscoveryClients',
                            '102', error_message)
                raise SDKException('EdiscoveryClients', '103')
            if not wait_for_job:
                return
            return self.wait_for_collection_job(wait_time=wait_time)
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def wait_for_collection_job(self, wait_time=60):
        """Waits for collection job to finish

                Args:

                    wait_time           (int)       --  time interval to wait for job completion in Mins
                                                            Default : 60Mins

                Return:

                    None

                Raises:

                    SDKException:

                            if collection job fails

                            if timeout happens

        """
        timeout = time.time() + 60 * wait_time  # 1hr
        while True:
            if time.time() > timeout:
                raise SDKException('EdiscoveryClients', '102', "Collection job Timeout")
            status = self.get_job_status()
            if int(status['state']) == InventoryConstants.CRAWL_JOB_COMPLETE_STATE:  # Finished State
                return
            elif int(status['state']) == InventoryConstants.CRAWL_JOB_COMPLETE_ERROR_STATE:  # completed with error
                raise SDKException('EdiscoveryClients', '102', "Job status is marked as Completed with Error")
            # STOPPING,STOPPED,ABORTING, ABORTED,EXCEPTION,UNKNOWN,SYNCING,PENDING
            elif int(status['state']) in InventoryConstants.CRAWL_JOB_FAILED_STATE:
                raise SDKException('EdiscoveryClients', '102', "Job status is marked as Failed/Error/Pending")
            else:
                time.sleep(10)

    def get_job_history(self):
        """Returns the job history details of ediscovery client

                Args:
                    None

                Returns:

                    list(dict)    --  containing job history details

                Raises:

                    SDKException:

                            if failed to get job history

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_JOBS_HISTORY % (self._client_id, self._type, self._data_source_id)
        )
        if flag:
            if response.json() and 'status' in response.json():
                return response.json()['status']
            elif 'error' in response.json():
                error = response.json()['error']
                error_code = error['errorCode']
                if error_code != 0:
                    error_message = error['errLogMessage']
                    raise SDKException(
                        'EdiscoveryClients',
                        '102', error_message)
                raise SDKException('EdiscoveryClients', '102', "Something went wrong while fetching job history")
            else:
                raise SDKException('EdiscoveryClients', '104')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_job_status(self):
        """Returns the job status details of this asset

                Args:
                    None

                Returns:

                    dict    --  containing job status details

                Raises:

                    SDKException:

                            if failed to get job status

        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_JOB_STATUS % (self._client_id, self._type, self._data_source_id)
        )
        if flag:
            if response.json() and 'status' in response.json():
                return response.json()['status']
            elif 'error' in response.json():
                error = response.json()['error']
                error_code = error['errorCode']
                if error_code != 0:
                    error_message = error['errLogMessage']
                    raise SDKException(
                        'EdiscoveryClients',
                        '102', error_message)
                raise SDKException('EdiscoveryClients', '102', "Something went wrong while fetching job status")
            else:
                raise SDKException('EdiscoveryClients', '105')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
