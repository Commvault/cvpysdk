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

"""File for operating on a Database Server Instances

DatabaseInstance is the only class defined in this file.

DatabaseInstance: Derived class from Instance Base class, representing a Database server instance,
                        and to perform operations on that instance

DatabaseInstance:

    __init__()                          --  initialise object of Database Instance associated with
                                            the specified agent

    _get_restore_to_disk_json()         --  Creates restore json for app free restore

    _get_source_item_app_free()         --  Generates list of source items
                                            based on job ids for app free restore

"""

from __future__ import unicode_literals
from base64 import b64encode

from ..instance import Instance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class DatabaseInstance(Instance):
    """
    Represents a specialized database instance derived from the Instance base class.

    This class is designed to manage and perform operations on database instances,
    providing methods for initialization, restore operations, and retrieval of source
    items for application-free backups. It facilitates interaction with backup jobs,
    disk restore processes, and source item management within the context of database
    instance operations.

    Key Features:
        - Initialization of database instance with agent, name, and ID
        - Generation of restore-to-disk JSON payloads for backup jobs
        - Retrieval of source items for application-free backup jobs

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int = None) -> None:
        """Initialize a DatabaseInstance object for a Sybase instance.

        Args:
            agent_object: Instance of the Agent class associated with this database instance.
            instance_name: Name of the Sybase database instance.
            instance_id: Optional; ID of the Sybase instance. Defaults to None.

        #ai-gen-doc
        """
        super(DatabaseInstance, self).__init__(
            agent_object, instance_name, instance_id)

    def _get_restore_to_disk_json(
        self,
        destination_client: str,
        destination_path: str,
        backup_job_ids: list,
        credentialName: str
    ) -> dict:
        """Create a JSON payload for application-free restore to disk.

        This method generates the required JSON structure for performing an application-free
        restore operation to a specified disk location on a destination client, using the
        provided backup job IDs and impersonation credentials.

        Args:
            destination_client: The name of the destination client where data will be restored.
            destination_path: The file system path on the destination client for the restore.
            backup_job_ids: List of backup job IDs to be used for the disk restore.
            credentialName: The saved credential name for impersonation on the destination client.

        Returns:
            dict: A dictionary representing the application-free restore JSON payload.

        Example:
            >>> restore_json = db_instance._get_restore_to_disk_json(
            ...     destination_client="client01",
            ...     destination_path="/restore/location",
            ...     backup_job_ids=[12345, 12346],
            ...     credentialName="oracle_cred"
            ... )
            >>> print(restore_json)
            # The returned dictionary can be used to initiate a restore operation.

        #ai-gen-doc
        """
        restore_json = self._restore_json(
            destination_client=destination_client,
            destination_path=destination_path,
            index_free_restore=True,
            restore_jobs=backup_job_ids,
            restore_to_disk=True,
            credentialName=credentialName
        )
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["jobIds"] = backup_job_ids
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "fileOption"]["sourceItem"] = self._get_source_item_app_free(backup_job_ids)
        return restore_json

    def _get_source_item_app_free(self, job_ids: list) -> list:
        """Generate a list of source items for application-free restore based on job IDs.

        Args:
            job_ids: List of job IDs (integers or strings) to be used for application-free restore.

        Returns:
            List of strings representing source items for the file option in application-free restore.

        #ai-gen-doc
        """
        commcell_id = self._commcell_object.commcell_id
        source_items = []
        for job_id in job_ids:
            single_item = "{0}:{1}".format(commcell_id, job_id)
            source_items.append(single_item)
        return source_items
