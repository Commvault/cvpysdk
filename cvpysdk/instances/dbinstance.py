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


class DatabaseInstance(Instance):
    """Derived class from Instance Base class, representing database instance,
        and to perform operations on that instance."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Initializes the object of Sybase Instance class
            Args:

                agent_object    (object) --  instance of the Agent class

                instance_name   (str)    --  name of the instance

                instance_id     (str)    --  id of the instance
                                             default None

            Returns :
                object - instance of the Sybase Instance class

        """
        super(DatabaseInstance, self).__init__(
            agent_object, instance_name, instance_id)

    def _get_restore_to_disk_json(self,
                                  destination_client,
                                  destination_path,
                                  backup_job_ids,
                                  user_name,
                                  password):
        """
        Creates restore json for app free restore

            Args:
                destination_client          (str)   --  destination client name

                destination_path            (str)   --  destination path for
                                                        application free restore

                backup_job_ids              (list)  --  list of backup job IDs
                                                        to be used for disk restore

                user_name                   (str)   --  impersonation user name
                                                        to restore to destination client

                password                    (str)   --  impersonation user password

            Returns:

                dict  -    returns app free restore json

        """
        encoded_password = b64encode(password.encode()).decode()
        restore_json = self._restore_json(
            destination_client=destination_client,
            destination_path=destination_path,
            index_free_restore=True,
            backup_job_ids=backup_job_ids,
            restore_to_disk=True,
            impersonate_user=user_name,
            impersonate_password=encoded_password
        )
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["jobIds"] = backup_job_ids
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "fileOption"]["sourceItem"] = self._get_source_item_app_free(backup_job_ids)
        return restore_json

    def _get_source_item_app_free(self, job_ids):
        """
        Generates list of source items based on job ids for app free restore
            Args:

                job_ids     (list)      --  list of job IDs for application free restore

            Returns:
                    (list)              -- list of strings representing source item for file option
        """
        commcell_id = self._commcell_object.commcell_id
        source_items = []
        for job_id in job_ids:
            single_item = "{0}:{1}".format(commcell_id, job_id)
            source_items.append(single_item)
        return source_items
