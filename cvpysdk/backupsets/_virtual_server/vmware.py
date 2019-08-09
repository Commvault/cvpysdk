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

    def __init__(self, instance_object, backupset_name, backupset_id=None):
        """Initialise the backupset object."""
        self._blr_pair_details = None
        super().__init__(instance_object, backupset_name, backupset_id)

    def refresh(self):
        """Refresh the properties of the Backupset."""
        super().refresh()
        self._blr_pair_details = _get_blr_pair_details(self._commcell_object)

    def get_blr_replication_pair(self, vm_name):
        """Fetches the BLR pair

        Args:
            vm_name      (str):  Name of the VM

        Returns:

            An instance of _BLRReplicationPair

        """
        try:
            return _BLRReplicationPair(self._commcell_object, vm_name, self._blr_pair_details[vm_name])
        except KeyError as error:
            raise SDKException(
                "Backupset",
                102,
                "Cannot find the VM with the given name[Names are case sensitive]") from error


class _BLRReplicationPair:
    """Class which performs all operations related to a BLR Pair"""
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

    def __init__(self, commcell, vmname, details):
        """Initializes the BLR Pair"""
        self._commcell = commcell
        self.vmname = vmname
        self._details = details

    def _make_request(self, payload):
        flag, response = self._commcell._cvpysdk_object.make_request(
            "PUT", self._commcell._services["CONTINUOUS_REPLICATION_MONITOR"], payload)

        try:
            assert response.json() == {"errorCode": 0}
        except (JSONDecodeError, AssertionError) as error:
            err_msg = "Failed to modify BLR pair state. %s", response.json().get("errorMessage", "") if flag else ""
            raise SDKException("Backupset", 102, err_msg) from error

    @property
    def status(self):
        """Returns the status of the BLR Pair"""
        try:
            self._details = _get_blr_pair_details(self._commcell)[self.vmname]
            return _BLRReplicationPair.Status(self._details["status"]).name.upper()
        except (AttributeError, KeyError):
            return _BLRReplicationPair.Status("DELETED")

    def resync(self):
        """Resyncs the pair"""
        self._details["status"] = _BLRReplicationPair.Status.resync.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def stop(self):
        """Stops the pair"""
        self._details["status"] = _BLRReplicationPair.Status.stop.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def suspend(self):
        """Suspends the pair"""
        self._details["status"] = _BLRReplicationPair.Status.suspend.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def start(self):
        """Starts the pair"""
        self._details["status"] = _BLRReplicationPair.Status.replicating.value
        self._make_request({"siteInfo": [self._details]})
        return self.status

    def resume(self):
        """Resumes the pair"""
        self.start()

    def delete(self):
        """Deletes the pair"""
        flag, response = self._commcell._cvpysdk_object.make_request(
            "DELETE", "%s/%s" % (self._commcell._services["CONTINUOUS_REPLICATION_MONITOR"], self._details["id"]))

        try:
            assert response.json() == {}
        except AssertionError as error:
            err_msg = "Failed to delete BLR pair. %s", response.json().get("errorMessage", "") if flag else ""
            raise SDKException("Backupset", 102, err_msg) from error

    def create_test_boot(self, vm_name, life_time=7200, esx_host_name=None, vm_network=None):
        """ Creates a test boot vm for the replication pair

        Args:
            vm_name             (str): Name of the test boot VM

            life_time           (int):  Life time of the VM  in seconds


            esx_host_name       (str): Name of the esx host on which VM must be created overriding the target esx

                Default: None

            vm_network:         (str): Name of the VM Network overriding the target network

                Default: None

        """
        request_dict = _BLRReplicationPair._boot_dict

        admin_options = self._get_admin_options(operation_type=1)
        admin_options["blockOperation"]["operations"]["vmBootInfo"] = self._get_vm_boot_info(vm_name, life_time, esx_host_name, vm_network)
        request_dict["TMMsg_CreateTaskReq"]["taskInfo"]["subTasks"]["options"]["adminOpts"] = admin_options

        self._send_xml(request_dict)

    def create_permanent_boot(self, vm_name, esx_host_name=None, vm_network=None):
        """ Creates a test boot vm for the replication pair

        Args:
            vm_name             (str): Name of the permanent boot VM

            esx_host_name       (str): Name of the esx host on which VM must be created overriding the target esx

                Default: None

            vm_network:         (str): Name of the VM Network overriding the target network

                Default: None


        """
        request_dict = _BLRReplicationPair._boot_dict

        admin_options = self._get_admin_options(operation_type=4)
        admin_options["blockOperation"]["operations"]["vmBootInfo"] = self._get_vm_boot_info(vm_name, 7200, esx_host_name, vm_network)
        request_dict["TMMsg_CreateTaskReq"]["taskInfo"]["subTasks"]["options"]["adminOpts"] = admin_options

        self._send_xml(request_dict)

    def _get_vm_boot_info(self, vm_name, lifetime, esx_host_name, vm_network):
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

    def _get_admin_options(self, operation_type):
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

    def _send_xml(self, request_dict):
        """Sends the boot request xml"""
        xml_payload = xmltodict.unparse(request_dict)
        response = self._commcell.execute_qcommand("qoperation execute", xml_payload)

        try:
            return response.json()["jobIds"][0]
        except (KeyError, JSONDecodeError) as error:
            raise SDKException("Backupset", 102,
                               "Boot was not successful. %s" % response.json().get("errorMessage", "")) from error
