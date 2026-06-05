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

"""Main file for performing VaultTracker policy operations.

VaultTrackerPolicies:   Class for representing all vault tracker policies of a tape library.

VaultTrackerPolicies:
    __init__(commcell_object,
             library_id,
             policies_dict)     --  initialize the collection with pre-fetched policy data

    __repr__()                  --  returns a string representation of the VaultTrackerPolicies instance

    all_vault_tracker_policies  --  property; returns the full policies dict

    has_vault_tracker_policy(policy_name)            --  checks if a vault tracker policy exists (case-insensitive)

    get_vault_tracker_policy(policy_name)            --  returns a VaultTrackerPolicy instance for the named policy

    delete_vault_tracker_policy(policy_name)         --  deletes the named vault tracker policy


VaultTrackerPolicy:   Class for representing a single VaultTracker policy.

VaultTrackerPolicy:
    __init__(commcell_object,
             policy_name,
             policy_id,
             library_id)    --  initialize the instance for a specific policy

    __repr__()              --  returns a string representation of the VaultTrackerPolicy instance

    run()                   --  runs the vault tracker policy and returns (task_id, job_id, action_id)

    _get_action_id()        --  fetches the vault tracker action ID for the running policy job

VaultTrackerPolicy instance Attributes:

    **policy_name**         --  returns the name of the vault tracker policy
    **policy_id**           --  returns the ID of the vault tracker policy
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import time
from typing import Dict, Optional, Tuple, TYPE_CHECKING

from ..exception import SDKException

if TYPE_CHECKING:
    from ..storage import TapeLibrary
    from ..commcell import Commcell


class VaultTrackerPolicies(object):
    """Collection class for all VaultTracker policies associated with a tape library.

    Obtained via the ``vault_tracker_policies`` property on a :class:`TapeLibrary` instance:

        >>> tape_library = commcell.tape_libraries.get("CommVault VirtualLib 39051")
        >>> vtp = tape_library.vault_tracker_policies
        >>> if vtp.has("my_policy"):
        ...     policy = vtp.get("my_policy")
        ...     task_id, job_id, action_id = policy.run()
    """

    def __init__(
        self,
        commcell_object: 'Commcell',
        tape_library: 'TapeLibrary',
    ) -> None:
        """Initialize VaultTrackerPolicies.

        Args:
            commcell_object:  Active Commcell instance.
            tape_library:     The :class:`TapeLibrary` instance this collection belongs to.
                              Policies are fetched directly from this object.
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._tape_library = tape_library
        self._library_id = int(tape_library.library_id)
        self._policies = {}
        self.refresh()

    def __repr__(self) -> str:
        return (
            f'VaultTrackerPolicies instance for library ID: {self._library_id} '
            f'of Commcell: "{self._commcell_object.commserv_name}"'
        )

    def refresh(self) -> None:
        """Refresh the internal policies by re-fetching from the tape library.

        Calls :meth:`TapeLibrary.refresh` to get the latest library properties, then
        repopulates the internal policies mapping.
        """
        self._tape_library.refresh()
        self._policies = self._tape_library._get_vault_tracker_policies_from_properties()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def all_vault_tracker_policies(self) -> Dict[str, Tuple[str, int]]:
        """Return the full policies mapping: ``{lower_name: (original_name, policy_id)}``."""
        return self._policies

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def has_vault_tracker_policy(self, policy_name: str) -> bool:
        """Check whether a vault tracker policy exists in this collection.

        Args:
            policy_name:  Name of the vault tracker policy (case-insensitive).

        Returns:
            bool: True if the policy exists, False otherwise.

        Raises:
            SDKException: If ``policy_name`` is not a string.
        """
        if not isinstance(policy_name, str):
            raise SDKException('Storage', '101', 'policy_name must be a string')
        return policy_name.lower() in self._policies

    def get(self, policy_name: str) -> 'VaultTrackerPolicy':
        """Return a :class:`VaultTrackerPolicy` instance for the named policy.

        Args:
            policy_name:  Name of the vault tracker policy (case-insensitive).

        Returns:
            VaultTrackerPolicy: Object with ``run()`` operation.

        Raises:
            SDKException: If ``policy_name`` is not a string or does not exist.
        """
        if not isinstance(policy_name, str):
            raise SDKException('Storage', '101', 'policy_name must be a string')
        key = policy_name.lower()
        if key not in self._policies:
            raise SDKException(
                'Storage', '102',
                f'VaultTrackerPolicy "{policy_name}" not found. '
                f'Available policies: {list(self._policies.keys())}'
            )
        original_name, policy_id = self._policies[key]
        return VaultTrackerPolicy(
            self._commcell_object,
            original_name,
            policy_id,
            self._library_id,
        )

    def delete(self, policy_name: str) -> None:
        """Delete a vault tracker policy by name.

        Calls DELETE /VaultTrackerPolicy/{policyId}

        Args:
            policy_name:  Name of the vault tracker policy to delete (case-insensitive).

        Raises:
            SDKException: If the policy is not found, the API call fails, or deletion is
                          unsuccessful.
        """
        if not isinstance(policy_name, str):
            raise SDKException('Storage', '101', 'policy_name must be a string')
        key = policy_name.lower()
        if key not in self._policies:
            raise SDKException(
                'Storage', '102',
                f'VaultTrackerPolicy "{policy_name}" not found. '
                f'Available policies: {list(self._policies.keys())}'
            )
        original_name, policy_id = self._policies[key]
        url = self._services['VAULT_TRACKER_POLICY'] % policy_id
        flag, response = self._commcell_object._cvpysdk_object.make_request('DELETE', url)

        self.refresh()
        if flag:
            resp_json = response.json() if response.text else {}
            error_code = resp_json.get('errorCode', 0)
            if error_code != 0:
                error_message = resp_json.get('errorMessage', 'Unknown error')
                raise SDKException(
                    'Storage', '102',
                    f'Failed to delete VaultTrackerPolicy "{original_name}". '
                    f'Error: {error_message}'
                )
            return
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)


class VaultTrackerPolicy(object):
    """Represents a single VaultTracker policy within a CommCell tape library.

    Obtained through :meth:`VaultTrackerPolicies.get`:

        >>> policy = tape_library.vault_tracker_policies.get("my_policy")
        >>> task_id, job_id, action_id = policy.run()
    """

    def __init__(
        self,
        commcell_object: 'Commcell',
        policy_name: str,
        policy_id: int,
        library_id: int,
    ) -> None:
        """Initialize a VaultTrackerPolicy instance.

        Args:
            commcell_object:  Active Commcell instance.
            policy_name:      Name of the vault tracker policy.
            policy_id:        Unique integer ID of the vault tracker policy (trackingPolicyId).
            library_id:       Integer ID of the tape library this policy belongs to.
                              Required to fetch vault tracker actions after a run.
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._policy_name = policy_name
        self._policy_id = int(policy_id)
        self._library_id = int(library_id)

    def __repr__(self) -> str:
        return (
            f'VaultTrackerPolicy instance for policy: "{self._policy_name}" '
            f'(ID: {self._policy_id}) of Commcell: "{self._commcell_object.commserv_name}"'
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def policy_name(self) -> str:
        """Name of the vault tracker policy."""
        return self._policy_name

    @property
    def policy_id(self) -> int:
        """Integer ID of the vault tracker policy."""
        return self._policy_id

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def run(self, timeout: int = 120) -> Tuple[int, str, Optional[int]]:
        """Run this vault tracker policy via the CreateTask API.

        Calls POST /CreateTask and then polls GET /V4/VaultTrackerAction?libraryId={library_id}
        until the resulting action ID appears or the timeout is reached.

        Args:
            timeout:  Maximum seconds to wait for the action ID to appear.
                      Defaults to 120 seconds.

        Returns:
            Tuple of (task_id, job_id, action_id) where:
                - task_id   (int):            Task ID returned by CreateTask.
                - job_id    (str):            Job ID string returned by CreateTask.
                - action_id (int or None):    VaultTracker action ID, or None if not found
                                              within the timeout.

        Raises:
            SDKException: If CreateTask call fails or returns an unexpected response.
        """
        payload = {
            "taskInfo": {
                "associations": [
                    {
                        "trackingPolicyId": self._policy_id,
                        "trackingPolicyName": self._policy_name,
                    }
                ],
                "task": {
                    "taskType": 1
                },
                "subTasks": [
                    {
                        "subTask": {
                            "operationType": 4010,
                            "subTaskType": 1,
                        },
                        "options": {
                            "adminOpts": {
                                "runvtPolicyOption": {
                                    "vTPolicy": {
                                        "trackingPolicyId": self._policy_id,
                                        "trackingPolicyName": self._policy_name,
                                    }
                                }
                            }
                        },
                    }
                ],
            }
        }

        create_task_url = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task_url, payload
        )

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        resp_json = response.json()
        if not resp_json:
            raise SDKException('Response', '102')

        task_id = resp_json.get('taskId')
        job_ids = resp_json.get('jobIds', [])
        job_id = str(job_ids[0]) if job_ids else None

        if task_id is None:
            raise SDKException(
                'Storage', '102',
                f'CreateTask did not return a taskId. Response: {resp_json}'
            )

        action_id = self._get_action_id(job_id=job_id, timeout=timeout)
        return task_id, job_id, action_id

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    def _get_action_id(self, job_id: Optional[str] = None, timeout: int = 120) -> Optional[int]:
        """Fetch the vault tracker action ID for the running policy job.

        Polls GET /V4/VaultTrackerAction?libraryId={library_id} until an action
        matching this policy (and optionally the job_id) appears, or the timeout
        is exceeded.

        Args:
            job_id:   Job ID string to match against actionList entries (optional).
                      When supplied, only actions whose jobId matches are considered.
            timeout:  Maximum seconds to poll. Defaults to 120.

        Returns:
            int: The actionId, or None if not found within the timeout.
        """
        url = self._services['GET_VAULT_TRACKER_ACTIONS'] % self._library_id
        deadline = time.time() + timeout
        poll_interval = 10

        while time.time() < deadline:
            flag, response = self._commcell_object._cvpysdk_object.make_request('GET', url)
            if flag and response.text:
                resp_json = response.json()
                actions = resp_json.get('vaultTrackerActionList', [])
                for action in actions:
                    # Match on policyId; optionally also match the jobId
                    if action.get('policyId') != self._policy_id:
                        continue
                    if job_id is not None and str(action.get('jobId', '')) != str(job_id):
                        continue
                    return action.get('actionId')

            time.sleep(poll_interval)

        return None
