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

"""
Main file for performing CommServe Recovery operations.

CommServeRecovery class is defined in this file.

CommServeRecovery:      Class for Commserve Recovery of a CS, and to perform operations related to Commserve Recovery


CommServeRecovery:
    __init__()                          --   initialize object of CommServeRecovery with the required CS GUID

    _get_backupsets()                   --   method to get the latest 5 backupsets that are shown on the cloud command

    _get_active_recovery_requests()     --   method to get all the recovery requests submitted for the CS

    _quota_details()                    --   returns the current recovery license status of the Commserv

    _create_cs_recovery_request()       --   returns the details of the given request ID

"""
from __future__ import absolute_import
from __future__ import unicode_literals

from json import JSONDecodeError
from datetime import datetime
from cvpysdk.exception import SDKException
from cvpysdk.commcell import Commcell


class CommServeRecovery:
    """Class to perform operations related to Commserve Recovery"""

    def __init__(self, commcell_object: Commcell, cs_guid: str):
        """Initialize the instance of the CommServeRecovery class.

            Args:
                commcell_object   (commcell object)    --  instance of the Commcell class

                cs_guid           (str)                --  CS GUID

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self.cs_guid = cs_guid
        self._CS_RECOVERY_API = self._services['COMMSERVE_RECOVERY']
        self._CS_RECOVERY_LICENSE_API = self._services['GET_COMMSERVE_RECOVERY_LICENSE_DETAILS'] % self.cs_guid
        self._CS_RECOVERY_RETENTION_API = self._services['GET_COMMSERVE_RECOVERY_RETENTION_DETAILS'] % self.cs_guid
        self._BACKUPSET_API = self._services['GET_BACKUPSET_INFO'] % self.cs_guid
        self._cleanup_lock_time = None
        self._is_licensed_commcell = self._quota_details().get('is_licensed')

        self._manual_retention_details()

    def _get_backupsets(self):
        """Returns details of uploaded backupsets"""
        flag, response = self._cvpysdk_object.make_request('GET', self._BACKUPSET_API)

        if flag:
            try:
                companies = response.json().get('companies')
                if not companies:
                    raise SDKException('CommserveRecovery', '101')
                return {
                    backupset_details["set_name"]: {
                        "set_id": backupset_details["set_id"],
                        "size": sum(int(files_details['size']) for files_details in backupset_details['files']),
                        "backup_time": datetime.strptime(backupset_details["time_modified"], "%Y-%m-%dT%H:%M:%SZ").timestamp(),
                        "manually_retained": bool(self._cleanup_lock_time),
                        "retained_until": self._cleanup_lock_time if self._cleanup_lock_time else None
                    }
                    for backupset_details in companies[0].get('commcells')[0].get('sets')
                }


            except (JSONDecodeError, KeyError):
                raise SDKException('Responcsse', '102', 'Job id not found in response')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _create_cs_recovery_request(self, set_name: str):
        """submits a new commserve recovery request and returns the request id to track"""
        try:
            set_id, set_size = self.backupsets[set_name]['set_id'], self.backupsets[set_name]['size']
        except KeyError:
            raise SDKException("CommserveRecovery", "104")
        payload = {
            "commcellGUID": self.cs_guid,
            "setId": set_id,
            "setName": set_name,
            "setSize": set_size
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._CS_RECOVERY_API, payload)

        if flag:
            try:
                if not response.json()['success']:
                    raise SDKException('Response', '101', 'request creation not successful')
                return response.json()['requestId']
            except (JSONDecodeError, KeyError):
                raise SDKException('Responcsse', '102', 'Job id not found in response')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _extend_recovery_request(self, request_id: int):
        """Returns True if the request is submitted successfully, otherwise, False"""
        payload = {
            "csGuid": self.cs_guid,
            "requestId": request_id,
            "operation": 2
        }
        flag, response = self._cvpysdk_object.make_request('PUT', self._CS_RECOVERY_API, payload)

        if flag:
            if response.json()['errorCode'] == 0:
                return True
            else:
                raise SDKException('Response', '102', 'request did not submit successfully')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_active_recovery_requests(self):

        url = f'{self._CS_RECOVERY_API}?csGuid={self.cs_guid}&showOnlyActiveRequests=true'

        states = {
            1: 'SUBMITTED',
            2: 'CREATING_VM',
            3: 'VM_CREATED',
            4: 'STAGING_CS',
            5: 'CS_STAGED',
            6: 'FINISHED',
            7: 'FAILED',
            8: 'KILLED'
        }

        flag, response = self._cvpysdk_object.make_request('GET', url)

        if flag:
            response = response.json()
            if response.get("errorCode") == 6:
                raise SDKException('CommserveRecovery', '101')

            map_vm_info = lambda vm_info: {
                                    "commandcenter_url": f"https://{vm_info['ipAddress']}/commandcenter",
                                    "vm_expiration_time": vm_info['vmExpirationTime'],
                                    "username": vm_info['credentials']['sUsername'],
                                    'password': vm_info['credentials']['sPassword']
                                }
            return {
                        request["id"]: {
                            "backupset": request.get("setName"),
                            "requestor": request["requestor"]["fullName"],
                            "version": request["servicePack"],
                            "start_time": request["createdTime"],
                            "end_time": request["vmInfo"]['vmExpirationTime'],
                            "status": states[request["status"]],
                            "vmInfo": map_vm_info(request['vmInfo']) if request['status'] == 5 else {}
                        }
                        for request in response.get('requests', [])
                    }

        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_vm_details(self, requestid: int):
        """Returns VM access details"""
        try:
            return self.active_recovery_requests[requestid]['vmInfo']
        except KeyError:
            raise SDKException('CommserveRecovery', '103')

    def _quota_details(self):
        """
        Returns CS Recovery license quota details in a dictionary
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._CS_RECOVERY_LICENSE_API)

        if flag:
            response = response.json()
            return {
                "is_licensed": response['license'],
                "start_date": datetime.strptime(response['quotaStartDate'], "%Y-%m-%dT%H:%M:%SZ").timestamp(),
                "end_date": datetime.strptime(response['quotaEndDate'], "%Y-%m-%dT%H:%M:%SZ").timestamp(),
                'used_recoveries_count': response['recoveriesCount'],
                'total_recoveries_allocated': response['maxRecoveries']
            }
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _manual_retention_details(self):
        """Returns details of used vs allocated quota of manual retains in a dict"""
        flag, response = self._cvpysdk_object.make_request('GET', self._CS_RECOVERY_RETENTION_API)
        if flag:
            response = response.json()
            self._cleanup_lock_time = response['cleanup_lock_time']
            return {
                "start_date": datetime.strptime(response['quota_start_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp(),
                "end_date": datetime.strptime(response['quota_end_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp(),
                'consumed_retains': response['consumed_retains'],
                'max_retains_allocated': response['max_retains']
            }
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    @property
    def is_licensed_commcell(self):
        return self._is_licensed_commcell

    @property
    def backupsets(self):
        return self._get_backupsets()

    @property
    def active_recovery_requests(self):
        return self._get_active_recovery_requests()

    @property
    def recovery_license_details(self):
        """
        Returns a dict containing start date, expiry date of license, number of consumed recovery requests and max requests count.
        Ex:
        {
                "is_licensed": 1,
                "start_date": 1711460013.0,
                "end_date": 1711460013.0,
                'used_recoveries_count': 23,
                'total_recoveries_allocated': 40
            }
        """
        return self._quota_details()

    @property
    def manual_retention_details(self):
        """
        Returns a dict containing start date, expiry date of license, number of consumed retains and max retains allocated.
        Ex:
        {
            "start_date": 1711460013,
            "end_date": 1711544749,
            'consumed_retains': 4,
            'max_retains_allocated': 10
        }
        """
        return self._manual_retention_details()

    def start_recovery(self, backupset_name: str):
        """
        Submits commserve recovery request for the given backupset
        Args:
            backupset_name (str) : name of the backup set to recover.
                                    Ex: SET_45
        Returns:
            Request id of the submitted request as an integer
        """
        return self._create_cs_recovery_request(backupset_name)

    def extend_reservation(self, request_id: int):
        """
        Extends the expiry time of a VM created for the given request id.
        Args:
            request_id (int) : commserve recovery request id
        Returns:
            True is the request is submitted successfully, otherwise, False
        """
        return self._extend_recovery_request(request_id)

    def get_vm_details(self, request_id: int):
        """
        Returns VM details for the given recovery request in a dict format.
        Ex:
        {
            "commandcenter_url": "https://20.235.143.244/commandcenter",
            "vm_expiration_time": 1712311000,
            "username": "recoverymanager",
            "password": "<REDACTED>",
        }
        """
        return self._get_vm_details(request_id)
