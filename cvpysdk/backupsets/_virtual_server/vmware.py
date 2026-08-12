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

"""Module for performing operations on a Backupset for the **VMWare Virtual Server** Agent."""
from enum import Enum
from json import JSONDecodeError

import xmltodict

from cvpysdk.backupsets.vsbackupset import VSBackupset
from cvpysdk.exception import SDKException
from typing import Any, Optional, Dict

def _get_blr_pair_details(commcell_object):
    """ Fetches all BLR Pair Details.
        This function is being used both by VMWareBackupset as well as _BLRReplicationPair


    Args:
        commcell_object (Commcell) :    Commcell object

    Returns:
        Dict containing vm name as key and its details as its value

    """
    flag, response = commcell_object._cvpysdk_object.make_request(
        "GET", commcell_object._services["CONTINUOUS_REPLICATION_MONITOR"])

    try:
        assert response.json()["summary"]["totalPairs"] != 0
        return {pair["sourceName"]: pair for pair in response.json()["siteInfo"]}
    except AssertionError:
        return None
    except (JSONDecodeError, KeyError) as error:
        err_msg = "Failed to fetch BLR pair details. %s", response.json().get("errorMessage", "") if flag else ""
        raise SDKException("Backupset", 102, err_msg) from error


class VMwareBackupset(VSBackupset):
    """
    VMwareBackupset class for managing VMware backup sets within a backup infrastructure.

    This class provides functionality to initialize, refresh, and manage VMware backup sets,
    including operations related to BLR (Block Level Replication) replication pairs for virtual machines.

    Key Features:
        - Initialization of VMware backup set objects with instance, name, and ID
        - Refreshing backup set information to ensure up-to-date state
        - Retrieval of BLR replication pair details for specified virtual machines

    #ai-gen-doc
    """

    def __init__(self, instance_object: Any, backupset_name: str, backupset_id: Optional[str] = None):
        """Initialize a VMwareBackupset object with the specified instance and backupset details.

        Args:
            instance_object: The instance object associated with the backupset. Type may vary depending on context.
            backupset_name: Name of the backupset as a string.
            backupset_id: Optional identifier for the backupset. If not provided, a default or auto-generated ID may be used.

        Example:
            >>> instance = Instance(...)
            >>> backupset = VMwareBackupset(instance, "VMBackupSet01", backupset_id="12345")
            >>> # The VMwareBackupset object is now initialized and ready for use

        #ai-gen-doc
        """
        self._blr_pair_details = None
        super().__init__(instance_object, backupset_name, backupset_id)

    def refresh(self) -> None:
        """Reload the properties of the VMware backupset.

        This method updates the backupset's internal state, ensuring that all properties 
        reflect the latest information from the Commcell, including BLR (Block Level Replication) pair details.

        Example:
            >>> backupset = VMwareBackupset(...)
            >>> backupset.refresh()  # Refreshes backupset properties from Commcell
            >>> # The backupset now contains updated BLR pair details and other properties

        #ai-gen-doc
        """
        super().refresh()
        self._blr_pair_details = _get_blr_pair_details(self._commcell_object)

    def get_blr_replication_pair(self, vm_name: str) -> '_BLRReplicationPair':
        """Retrieve the BLR replication pair for a specified virtual machine.

        Args:
            vm_name: Name of the virtual machine for which to fetch the BLR replication pair. 
                Note: VM names are case sensitive.

        Returns:
            _BLRReplicationPair: An instance representing the BLR replication pair for the given VM.

        Raises:
            SDKException: If the specified VM name does not exist in the backupset.

        Example:
            >>> backupset = VMwareBackupset(commcell_object, ...)
            >>> blr_pair = backupset.get_blr_replication_pair('VM01')
            >>> print(f"BLR Pair for VM01: {blr_pair}")
            >>> # The returned _BLRReplicationPair object can be used for further replication operations

        #ai-gen-doc
        """
        try:
            return _BLRReplicationPair(self._commcell_object, vm_name, self._blr_pair_details[vm_name])
        except KeyError as error:
            raise SDKException(
                "Backupset",
                102,
                "Cannot find the VM with the given name[Names are case sensitive]") from error


class _BLRReplicationPair:
    """
    Manages operations related to a BLR (Block Level Replication) Pair.

    This class provides a comprehensive interface for handling BLR replication pairs,
    including lifecycle management, status monitoring, and boot operations for virtual machines.
    It interacts with the underlying infrastructure to perform actions such as starting,
    stopping, suspending, resuming, and deleting replication pairs, as well as initiating
    test and permanent boot operations for VMs.

    Key Features:
        - Initialization with commcell, VM name, and details
        - Status monitoring via property
        - Lifecycle management: start, stop, suspend, resume, resync, and delete operations
        - Creation of test and permanent VM boots with configurable parameters
        - Retrieval of VM boot information and administrative options
        - Internal request handling and XML communication for backend operations

    #ai-gen-doc
    """
    _boot_dict = {
        "TMMsg_CreateTaskReq": {
            "taskInfo": {
                "task": {
                    "taskFlags": {
                        "disabled": "0"
                    },
                    "taskType": "1",
                    "ownerId": "1",
                    "initiatedFrom": "1",
                    "ownerName": "admin"
                },
                "subTasks": {
                    "subTask": {
                        "subTaskType": "1",
                        "operationType": "4047"
                    },
                    "options": {
                        "backupOpts": {
                            "mediaOpt": {
                                "auxcopyJobOption": {
                                    "useMaximumStreams": "1",
                                    "maxNumberOfStreams": "0",
                                    "allCopies": "1",
                                    "useScallableResourceManagement": "0"
                                }
                            }
                        },
                        "adminOpts": {},

                    },
                    "subTaskOperation": "1"
                }
            }
        }
    }

    class Status(Enum):
        """Enum for BLR pair status"""
        backup = 1
        restoring = 2
        resync = 3
        replicating = 4
        suspend = 5
        stop = 6
        starting = 10
        stopping = 11
        resuming = 13

    def __init__(self, commcell: 'Commcell', vmname: str, details: Dict[str, Any]) -> None:
        """Initialize a BLRReplicationPair instance for a specific virtual machine.

        Args:
            commcell: Instance of the Commcell class representing the backup environment.
            vmname: Name of the virtual machine as a string.
            details: Dictionary containing BLR pair configuration details.

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> vmname = "VM_Production01"
            >>> details = {"replication_type": "async", "target_site": "DR_Site"}
            >>> blr_pair = _BLRReplicationPair(commcell, vmname, details)
            >>> print(f"BLR Pair created for VM: {blr_pair.vmname}")
        #ai-gen-doc
        """
        self._commcell = commcell
        self.vmname = vmname
        self._details = details

    def _make_request(self, payload: Dict[str, Any]) -> None:
        """Send a PUT request to modify the BLR replication pair state.

        This method sends a request to the continuous replication monitor service using the provided payload.
        If the response does not indicate success, an SDKException is raised.

        Args:
            payload: Dictionary containing the request payload for the BLR pair modification.

        Raises:
            SDKException: If the request fails or the response contains an error.

        Example:
            >>> payload = {"pairId": 123, "action": "pause"}
            >>> blr_pair = _BLRReplicationPair(...)
            >>> blr_pair._make_request(payload)
            >>> # If the request is successful, no exception is raised.
            >>> # If there is an error, SDKException will be raised.

        #ai-gen-doc
        """
        flag, response = self._commcell._cvpysdk_object.make_request(
            "PUT", self._commcell._services["CONTINUOUS_REPLICATION_MONITOR"], payload)

        try:
            assert response.json() == {"errorCode": 0}
        except (JSONDecodeError, AssertionError) as error:
            err_msg = "Failed to modify BLR pair state. %s", response.json().get("errorMessage", "") if flag else ""
            raise SDKException("Backupset", 102, err_msg) from error

    @property
    def status(self) -> str:
        """Get the current status of the BLR (Block Level Replication) Pair.

        Returns:
            The status of the BLR Pair as an uppercase string. Possible values include statuses such as "ACTIVE", "INACTIVE", or "DELETED".

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> current_status = pair.status  # Use dot notation for property access
            >>> print(f"BLR Pair status: {current_status}")
            >>> # The returned status string can be used for monitoring or reporting

        #ai-gen-doc
        """
        try:
            self._details = _get_blr_pair_details(self._commcell)[self.vmname]
            return _BLRReplicationPair.Status(self._details["status"]).name.upper()
        except (AttributeError, KeyError):
            return _BLRReplicationPair.Status("DELETED")

    def resync(self) -> str:
        """Initiate a resynchronization operation for the replication pair.

        This method updates the status of the replication pair to 'resync' and sends a request to perform the resynchronization.
        After the operation, it returns the current status of the pair.

        Returns:
            The status of the replication pair after resynchronization as a string.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> result = pair.resync()
            >>> print(f"Replication pair status: {result}")
            >>> # The status should reflect the resync operation

        #ai-gen-doc
        """
        self._details["status"] = _BLRReplicationPair.Status.resync.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def stop(self) -> str:
        """Stop the replication pair and update its status.

        This method sets the status of the replication pair to 'stop' and sends a request to apply the change.
        It then returns the current status of the pair.

        Returns:
            The updated status of the replication pair as a string.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> status = pair.stop()
            >>> print(f"Replication pair stopped. Current status: {status}")

        #ai-gen-doc
        """
        self._details["status"] = _BLRReplicationPair.Status.stop.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def suspend(self) -> str:
        """Suspend the replication pair.

        This method updates the status of the replication pair to 'suspend' and sends a request to apply the change.
        The current status of the pair is returned after the operation.

        Returns:
            The status of the replication pair as a string after suspension.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> status = pair.suspend()
            >>> print(f"Replication pair status: {status}")
            >>> # The status should indicate the pair is now suspended

        #ai-gen-doc
        """
        self._details["status"] = _BLRReplicationPair.Status.suspend.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def start(self) -> str:
        """Start the BLR replication pair and update its status.

        This method initiates the replication process for the pair by updating its status
        and making the necessary request to begin replication.

        Returns:
            The current status of the replication pair as a string.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> status = pair.start()
            >>> print(f"Replication pair status: {status}")
            >>> # The status should reflect that replication has started

        #ai-gen-doc
        """
        self._details["status"] = _BLRReplicationPair.Status.replicating.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def resume(self) -> None:
        """Resume the replication pair operation.

        This method resumes the replication process for the current pair, 
        typically after it has been paused or stopped.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> pair.resume()
            >>> print("Replication pair resumed successfully")
        #ai-gen-doc
        """
        self.start()

    def delete(self) -> None:
        """Delete the BLR replication pair from the Commcell.

        This method sends a DELETE request to remove the specified BLR replication pair.
        If the deletion fails, an SDKException is raised with the error details.

        Raises:
            SDKException: If the BLR replication pair could not be deleted.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> pair.delete()
            >>> print("BLR replication pair deleted successfully")

        #ai-gen-doc
        """
        flag, response = self._commcell._cvpysdk_object.make_request(
            "DELETE", "%s/%s" % (self._commcell._services["CONTINUOUS_REPLICATION_MONITOR"], self._details["id"]))

        try:
            assert response.json() == {}
        except AssertionError as error:
            err_msg = "Failed to delete BLR pair. %s", response.json().get("errorMessage", "") if flag else ""
            raise SDKException("Backupset", 102, err_msg) from error

    def create_test_boot(self, vm_name: str, life_time: int = 7200, esx_host_name: Optional[str] = None, vm_network: Optional[str] = None) -> None:
        """Create a test boot virtual machine for the replication pair.

        This method initiates the creation of a test boot VM using the specified parameters. 
        The VM is created for testing purposes and will exist for the defined lifetime.

        Args:
            vm_name: Name of the test boot VM to be created.
            life_time: Lifetime of the VM in seconds. Defaults to 7200 seconds (2 hours).
            esx_host_name: Optional name of the ESX host on which the VM should be created, overriding the default target ESX host.
            vm_network: Optional name of the VM network to use, overriding the default target network.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> pair.create_test_boot("TestBootVM", life_time=3600, esx_host_name="esx01.local", vm_network="VM_Network_1")
            >>> # This will create a test boot VM named "TestBootVM" on the specified ESX host and network for 1 hour.

        #ai-gen-doc
        """
        request_dict = _BLRReplicationPair._boot_dict

        admin_options = self._get_admin_options(operation_type=1)
        admin_options["blockOperation"]["operations"]["vmBootInfo"] = self._get_vm_boot_info(vm_name, life_time, esx_host_name, vm_network)
        request_dict["TMMsg_CreateTaskReq"]["taskInfo"]["subTasks"]["options"]["adminOpts"] = admin_options

        self._send_xml(request_dict)

    def create_permanent_boot(self, vm_name: str, esx_host_name: Optional[str] = None, vm_network: Optional[str] = None) -> None:
        """Create a permanent boot virtual machine for the replication pair.

        This method initiates the creation of a permanent boot VM using the specified parameters.
        Optionally, you can override the target ESX host and VM network.

        Args:
            vm_name: Name of the permanent boot VM to be created.
            esx_host_name: Optional; name of the ESX host on which the VM should be created. If not provided, the target ESX is used.
            vm_network: Optional; name of the VM network to override the target network. If not provided, the default network is used.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> pair.create_permanent_boot("PermanentBootVM")
            >>> pair.create_permanent_boot("PermanentBootVM", esx_host_name="esx01.local", vm_network="Production_Network")

        #ai-gen-doc
        """
        request_dict = _BLRReplicationPair._boot_dict

        admin_options = self._get_admin_options(operation_type=4)
        admin_options["blockOperation"]["operations"]["vmBootInfo"] = self._get_vm_boot_info(vm_name, 7200, esx_host_name, vm_network)
        request_dict["TMMsg_CreateTaskReq"]["taskInfo"]["subTasks"]["options"]["adminOpts"] = admin_options

        self._send_xml(request_dict)

    def _get_vm_boot_info(self, vm_name: str, lifetime: int, esx_host_name: Optional[str], vm_network: str) -> Dict[str, Any]:
        """Generate VM boot information for BLR replication.

        Args:
            vm_name: Name to assign to the new virtual machine.
            lifetime: Lifetime of the VM in seconds.
            esx_host_name: Name of the ESX host where the VM will be booted. If None, an empty string is used.
            vm_network: Name of the network to attach to the VM.

        Returns:
            Dictionary containing VM boot configuration details required for BLR replication.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> boot_info = pair._get_vm_boot_info("TestVM", 3600, "esx01.local", "VM Network")
            >>> print(boot_info)
            >>> # The returned dictionary can be used for VM boot operations

        #ai-gen-doc
        """
        return {"vmUUId": self._details["sourceGuid"],
                "vmName": self._details["sourceName"],
                "newVmName": vm_name,
                "bootFromLatestPointInTime": "0",
                "bootFromOldestPointInTime": "1",
                "rpTimeOfDay": "-1",
                "lifeTimeInSec": lifetime,
                "blrPairId": self._details["id"],
                "hostname": esx_host_name or "",
                "networkCards": {"name": vm_network, "label": "Network adapter 1"}
                }

    def _get_admin_options(self, operation_type: str) -> Dict[str, Any]:
        """Generate administrative options for a block operation.

        Args:
            operation_type: The type of operation to perform, specified as a string.

        Returns:
            Dictionary containing administrative options for the block operation, including VM boot info,
            application ID, destination proxy client ID, job ID, and operation type.

        Example:
            >>> pair = _BLRReplicationPair(...)
            >>> options = pair._get_admin_options("start")
            >>> print(options)
            {'blockOperation': {'operations': {'vmBootInfo': {}, 'appId': '206', 'dstProxyClientId': ..., 'jobId': '0', 'opType': 'start'}}}

        #ai-gen-doc
        """
        return {
            "blockOperation": {
                "operations": {
                    "vmBootInfo": {},
                    "appId": "206",
                    "dstProxyClientId": self._details["tailClientId"],
                    "jobId": "0",
                    "opType": operation_type
                }
            }
        }

    def _send_xml(self, request_dict: Dict[str, Any]) -> int:
        """Send the boot request XML to the Commcell and retrieve the job ID.

        This method serializes the provided request dictionary into XML format,
        sends it to the Commcell using the 'qoperation execute' command, and
        returns the job ID of the initiated operation. If the response does not
        contain a valid job ID, an SDKException is raised with the error message.

        Args:
            request_dict: Dictionary containing the boot request parameters to be serialized as XML.

        Returns:
            The job ID (as an integer) of the initiated boot operation.

        Raises:
            SDKException: If the response does not contain a valid job ID or if there is an error in the response.

        Example:
            >>> request = {
            ...     "bootRequest": {
            ...         "clientName": "TestClient",
            ...         "backupsetName": "TestBackupset"
            ...     }
            ... }
            >>> pair = _BLRReplicationPair(...)
            >>> job_id = pair._send_xml(request)
            >>> print(f"Boot job started with ID: {job_id}")

        #ai-gen-doc
        """
        xml_payload = xmltodict.unparse(request_dict)
        response = self._commcell.execute_qcommand("qoperation execute", xml_payload)

        try:
            return response.json()["jobIds"][0]
        except (KeyError, JSONDecodeError) as error:
            raise SDKException("Backupset", 102,
                               "Boot was not successful. %s" % response.json().get("errorMessage", "")) from error
