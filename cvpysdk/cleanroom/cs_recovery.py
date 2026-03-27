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

from datetime import datetime
from json import JSONDecodeError
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from cvpysdk.commcell import Commcell

from cvpysdk.exception import SDKException


class CommServeRecovery:
    """
    Class to perform operations related to CommServe Recovery.

    This class provides a comprehensive interface for managing CommServe recovery operations,
    including backupset management, recovery request lifecycle, VM details retrieval, quota and
    retention information, and license validation. It is designed to facilitate the recovery
    process in a Commcell environment by offering methods to initiate, extend, and close recovery
    requests, as well as to access relevant details and properties associated with recovery tasks.

    Key Features:
        - Initialization with Commcell object and CommServe GUID
        - Retrieval of backupsets and active recovery requests
        - Creation, extension, and closure of CommServe recovery requests
        - Access to VM details associated with recovery requests
        - Quota and manual retention details management
        - Properties for license validation, backupsets, active requests, recovery license, and retention details
        - Methods to start, extend, and close recovery reservations

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', cs_guid: str) -> None:
        """Initialize a new instance of the CommServeRecovery class.

        Args:
            commcell_object: An instance of the Commcell class representing the Commcell connection.
            cs_guid: The unique GUID string identifying the CommServe.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> cs_guid = "1234-5678-90ab-cdef"
            >>> cs_recovery = CommServeRecovery(commcell, cs_guid)
            >>> print("CommServeRecovery instance created successfully")

        #ai-gen-doc
        """
        try:
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
        except Exception as e:
            raise SDKException('CommserveRecovery', '105', "Failed to initialize CommServeRecovery") from e

    def _get_backupsets(self) -> dict:
        """Retrieve details of uploaded backupsets.

        Returns:
            list: A list containing information about each uploaded backupset.

        Example:
            >>> recovery = CommServeRecovery()
            >>> backupsets = recovery._get_backupsets()
            >>> print(f"Number of backupsets: {len(backupsets)}")
            >>> # Each item in the list represents a backupset's details

        #ai-gen-doc
        """
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

    def _create_cs_recovery_request(self, set_name: str, address_prefixes: list, remember_address: bool) -> int:
        """Submit a new CommServe recovery request.

        This method initiates a CommServe recovery operation using the specified set name and address prefixes.
        It returns a unique request ID that can be used to track the progress or status of the recovery request.

        Args:
            set_name: The name of the recovery set to use for the operation.
            address_prefixes: A list of address prefixes to be used during the recovery process.
            remember_address: If True, the addresses will be remembered for future recovery operations.

        Returns:
            An integer representing the unique request ID for the submitted CommServe recovery request.

        Example:
            >>> recovery = CommServeRecovery()
            >>> request_id = recovery._create_cs_recovery_request(
            ...     set_name="RecoverySet1",
            ...     address_prefixes=["192.168.1.0/24", "10.0.0.0/8"],
            ...     remember_address=True
            ... )
            >>> print(f"Recovery request submitted with ID: {request_id}")

        #ai-gen-doc
        """
        try:
            set_id, set_size = self.backupsets[set_name]['set_id'], self.backupsets[set_name]['size']
        except KeyError:
            raise SDKException("CommserveRecovery", "104")
        payload = {
            "commcellGUID": self.cs_guid,
            "setId": set_id,
            "setName": set_name,
            "setSize": set_size,
            "addressPrefixes": address_prefixes,
            "rememberAddress": remember_address
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._CS_RECOVERY_API, payload)

        if flag:
            try:
                if not response.json()['success']:
                    raise SDKException('Response', '101', 'request creation not successful')
                return response.json()['requestId']
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102', 'Job id not found in response')
        else:
            raise SDKException('CommserveRecovery', '105', "Failed to create recovery request")

    def _extend_recovery_request(self, request_id: int) -> bool:
        """Extend the recovery request for the specified request ID.

        Args:
            request_id: The unique identifier of the recovery request to be extended.

        Returns:
            True if the extension request is submitted successfully; otherwise, False.

        Example:
            >>> recovery = CommServeRecovery()
            >>> success = recovery._extend_recovery_request(12345)
            >>> print(f"Extension submitted: {success}")

        #ai-gen-doc
        """
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
            raise SDKException('CommserveRecovery', '105', "Failed to extend recovery request")

    def _close_recovery_request(self, request_id: int) -> bool:
        """Submit a request to close a CommServe recovery operation.

        Args:
            request_id: The unique identifier of the recovery request to be closed.

        Returns:
            True if the close request is submitted successfully; otherwise, False.

        Example:
            >>> recovery = CommServeRecovery()
            >>> success = recovery._close_recovery_request(12345)
            >>> print(f"Request closed: {success}")

        #ai-gen-doc
        """
        payload = {
            "csGuid": self.cs_guid,
            "requestId": request_id,
            "operation": 3
        }
        flag, response = self._cvpysdk_object.make_request('PUT', self._CS_RECOVERY_API, payload)

        if flag:
            if response.json()['errorCode'] == 0:
                return True
            else:
                raise SDKException('Response', '102', 'request did not submit successfully')
        else:
            raise SDKException('CommserveRecovery', '105', "Failed to close recovery request")

    def _get_active_recovery_requests(self, staged:bool=True) -> list:
        """Retrieve the list of currently active CommServe recovery requests.

        Args:
            staged: If True, retrieves only active requests. If False, retrieves all requests. Defaults to True.

        Returns:
            list: A list containing details of all active CommServe recovery requests.

        Example:
            >>> recovery = CommServeRecovery()
            >>> active_requests = recovery._get_active_recovery_requests()
            >>> print(f"Number of active recovery requests: {len(active_requests)}")
            >>> # Each item in the list represents an active recovery request

        #ai-gen-doc
        """

        url = f'{self._CS_RECOVERY_API}?csGuid={self.cs_guid}&showOnlyActiveRequests={staged}'

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

            map_vm_info = lambda request: {
                                    "commandcenter_url": f"https://{request['vmInfo']['ipAddress']}/commandcenter" if request['status'] == 5 else '',
                                    "vm_expiration_time": request['vmInfo']['vmExpirationTime'],
                                    "username": request['vmInfo'].get('credentials',{}).get('sUsername'),
                                    'password': request['vmInfo'].get('credentials',{}).get('sPassword'),
                                    'vmName': request['vmInfo'].get('name')
                                }
            return {
                        request["id"]: {
                            "backupset": request.get("setName"),
                            "requestor": request["requestor"]["fullName"],
                            "version": request["servicePack"],
                            "start_time": request["createdTime"],
                            "end_time": request["vmInfo"]['vmExpirationTime'],
                            "status": states[request["status"]],
                            "vmInfo": map_vm_info(request)
                        }
                        for request in response.get('requests', [])
                    }

        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_vm_details(self, requestid: int, staged:bool=True) -> dict:
        """Retrieve access details for a virtual machine associated with a specific request ID.

        Args:
            requestid: The unique identifier for the VM access request.
            staged: If True, retrieves from cached active requests. If False, makes fresh API call.

        Returns:
            A dictionary containing the VM access details, such as connection information and credentials.

        Example:
            >>> recovery = CommServeRecovery()
            >>> vm_details = recovery._get_vm_details(12345)
            >>> print(vm_details)
            {'ip': '192.168.1.10', 'username': 'admin', 'password': '*****'}

        #ai-gen-doc
        """
        try:
            if staged:
                return self.active_recovery_requests[requestid]['vmInfo']
            return self._get_active_recovery_requests(staged=False)[requestid]['vmInfo']
        except KeyError:
            raise SDKException('CommserveRecovery', '103')

    def _quota_details(self) -> dict:
        """Retrieve the CommServe Recovery license quota details.

        Returns:
            dict: A dictionary containing the quota details for the CS Recovery license.

        Example:
            >>> recovery = CommServeRecovery()
            >>> quota_info = recovery._quota_details()
            >>> print(quota_info)
            {'total_quota': 100, 'used_quota': 45, 'remaining_quota': 55}

        #ai-gen-doc
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

    def _manual_retention_details(self) -> dict:
        """Retrieve details about the used versus allocated quota of manual retains.

        Returns:
            dict: A dictionary containing information about the quota usage for manual retains,
            including both used and allocated values.

        Example:
            >>> recovery = CommServeRecovery()
            >>> retention_info = recovery._manual_retention_details()
            >>> print(f"Used quota: {retention_info['used']}, Allocated quota: {retention_info['allocated']}")

        #ai-gen-doc
        """
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
    def is_licensed_commcell(self) -> bool:
        """Check if the Commcell is licensed for CommServe Recovery operations.

        Returns:
            True if the Commcell is licensed for CommServe Recovery; False otherwise.

        Example:
            >>> recovery = CommServeRecovery(commcell_object)
            >>> if recovery.is_licensed_commcell:
            ...     print("Commcell is licensed for CommServe Recovery.")
            ... else:
            ...     print("Commcell is not licensed for CommServe Recovery.")

        #ai-gen-doc
        """
        return self._is_licensed_commcell

    @property
    def backupsets(self) -> Dict[str, dict]:
        """Get the details of backupsets.

        Returns:
            Dict[str, dict]: A dictionary where each key is a backupset name and the value is another dictionary containing backupset details.

        Example:
            >>> recovery = CommServeRecovery(commcell_object)
            >>> backupsets = recovery.backupsets  # Access the backupsets property
            >>> for name, details in backupsets.items():
            ...     print(f"Backupset Name: {name}, Details: {details}")

        #ai-gen-doc
        """
        return self._get_backupsets()

    @property
    def active_recovery_requests(self) -> list:
        """Get the list of currently active CommServe recovery requests.

        Returns:
            list: A list containing details of all active CommServe recovery requests.

        Example:
            >>> recovery = CommServeRecovery()
            >>> active_requests = recovery.active_recovery_requests
            >>> print(f"Number of active recovery requests: {len(active_requests)}")
            >>> # Each item in the list represents an active recovery request

        #ai-gen-doc
        """
        return self._get_active_recovery_requests()

    @property
    def recovery_license_details(self) -> dict:
        """Get the CommServe recovery license details.

        Returns:
            dict: A dictionary containing license information, including:
                - is_licensed (int): 1 if licensed, 0 otherwise.
                - start_date (float): License start date as a Unix timestamp.
                - end_date (float): License expiry date as a Unix timestamp.
                - used_recoveries_count (int): Number of recovery requests consumed.
                - total_recoveries_allocated (int): Maximum number of recovery requests allowed.

        Example:
            >>> recovery = CommServeRecovery()
            >>> license_info = recovery.recovery_license_details
            >>> print(license_info)
            {
                "is_licensed": 1,
                "start_date": 1711460013.0,
                "end_date": 1711460013.0,
                "used_recoveries_count": 23,
                "total_recoveries_allocated": 40
            }

        #ai-gen-doc
        """
        return self._quota_details()

    @property
    def manual_retention_details(self) -> Dict[str, int]:
        """Get manual retention details for the CommServe license.

        Returns:
            Dict[str, int]: A dictionary containing the following keys:
                - "start_date": The start date of the license (as a Unix timestamp).
                - "end_date": The expiry date of the license (as a Unix timestamp).
                - "consumed_retains": The number of retains that have been consumed.
                - "max_retains_allocated": The maximum number of retains allocated.

        Example:
            >>> recovery = CommServeRecovery()
            >>> details = recovery.manual_retention_details
            >>> print(details)
            {'start_date': 1711460013, 'end_date': 1711544749, 'consumed_retains': 4, 'max_retains_allocated': 10}

        #ai-gen-doc
        """
        return self._manual_retention_details()

    def start_recovery(self, backupset_name: str, address_prefixes: str = "*", remember_address: bool = True) -> int:
        """Submit a CommServe recovery request for the specified backup set.

        This method initiates a recovery operation for the given backup set name, using the provided
        address prefixes and an option to remember the address for future use. The method returns
        the request ID of the submitted recovery operation.

        Args:
            backupset_name: The name of the backup set to recover (e.g., "SET_45").
            address_prefixes: Address prefixes to use for the recovery. Use "*" to include all addresses.
                Defaults to "*".
            remember_address: Whether to remember the address for future recovery operations.
                Defaults to True.

        Returns:
            The request ID (as an integer) of the submitted CommServe recovery request.

        Example:
            >>> recovery = CommServeRecovery()
            >>> request_id = recovery.start_recovery("SET_45", address_prefixes="192.168.*", remember_address=True)
            >>> print(f"Recovery request submitted with ID: {request_id}")

        #ai-gen-doc
        """
        return self._create_cs_recovery_request(backupset_name, address_prefixes, remember_address)

    def extend_reservation(self, request_id: int) -> bool:
        """Extend the expiry time of a VM created for a specific CommServe recovery request.

        Args:
            request_id: The unique identifier of the CommServe recovery request for which the VM reservation should be extended.

        Returns:
            True if the reservation extension request is submitted successfully; otherwise, False.

        Example:
            >>> recovery = CommServeRecovery()
            >>> success = recovery.extend_reservation(12345)
            >>> if success:
            ...     print("Reservation extended successfully.")
            ... else:
            ...     print("Failed to extend reservation.")

        #ai-gen-doc
        """
        return self._extend_recovery_request(request_id)

    def close_reservation(self, request_id: int) -> bool:
        """Close the current CommServe recovery request and release the associated VM.

        This method submits a request to close an active CommServe recovery session,
        releasing any virtual machine resources that were allocated for the recovery process.

        Args:
            request_id: The unique identifier of the CommServe recovery request to be closed.

        Returns:
            True if the request to close the reservation is submitted successfully; otherwise, False.

        Example:
            >>> recovery = CommServeRecovery()
            >>> success = recovery.close_reservation(12345)
            >>> print(f"Reservation closed: {success}")

        #ai-gen-doc
        """
        return self._close_recovery_request(request_id)

    def get_vm_details(self, request_id: int, staged=True) -> dict:
        """Retrieve VM details for a specific recovery request.

        Given a recovery request ID, this method returns a dictionary containing
        details about the associated virtual machine, such as the Command Center URL,
        VM expiration time, username, and password.

        Args:
            request_id: The unique identifier for the recovery request.
            staged: If True, retrieves from cached active requests. If False, makes fresh API call. Defaults to True.

        Returns:
            dict: A dictionary with VM details, for example:
                {
                    "commandcenter_url": "https://20.235.143.244/commandcenter",
                    "vm_expiration_time": 1712311000,
                    "username": "recoverymanager",
                    "password": "<REDACTED>",
                }

        Example:
            >>> recovery = CommServeRecovery()
            >>> vm_info = recovery.get_vm_details(12345)
            >>> print(vm_info["commandcenter_url"])
            https://20.235.143.244/commandcenter

        #ai-gen-doc
        """
        return self._get_vm_details(request_id, staged)
