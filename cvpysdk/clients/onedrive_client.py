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
OneDriveClient class is defined in this file.

OneDriveClient:     Class for a single OneDrive for Business client (v2) of the commcell

OneDriveClient
=======

_get_subclient() --  Returns the sub-client object for OneDrive for Business client (v2)

backup_all_users_in_client() -- Run backup for all users present in OneDrive for Business client (v2)

in_place_restore()  --  Run an inplace restore of specified users for OneDrive for business client (v2)

out_of_place_restore()  --  Run an out-of-place restore of specified users for OneDrive for business client (v2)

disk_restore()  --  Runs disk restore of specified users for OneDrive for business client (v2)

modify_server_plan()  --  Method to Modify Server Plan Associated to Client

modify_job_results_directory()  --  Method to modify job results directory

"""

from ..client import Client


class OneDriveClient(Client):
    def __init__(self, commcell_object, client_name, client_id=None):
        """Initialise the OneDrive Client class instance.

            Args:
                commcell_object (object)     --  instance of the Commcell class

                client_name     (str)        --  name of the client

                client_id       (str)        --  id of the client
                                                default: None

            Returns:
                object - instance of the OneDrive Client class
        """
        super(OneDriveClient, self).__init__(commcell_object, client_name, client_id)

    def _get_subclient(self):
        """ Returns the sub-client object for OneDrive for Business client

            Returns:
                _subclient (object) -   Subclient object

        """
        _client = self._commcell_object.clients.get(self.client_name)
        _agent = _client.agents.get('Cloud Apps')
        _instance = _agent.instances.get('OneDrive')
        _backupset = _instance.backupsets.get('defaultbackupset')
        _subclient = _backupset.subclients.get('default')
        return _subclient

    def backup_all_users_in_client(self):
        """ Run backup for all users present in OneDrive client

            Returns:
                object - instance of the Job class for this backup job
        """
        _subclient_object = self._get_subclient()
        return _subclient_object.backup(backup_level='INCREMENTAL')

    def in_place_restore(self, users, **kwargs):
        """ Run an inplace restore of specified users for OneDrive for business client

            Args:
                users (list) :  List of SMTP addresses of users
                **kwargs (dict) : Additional parameters
                    overwrite (bool) : unconditional overwrite files during restore (default: False)
                    restore_as_copy (bool) : restore files as copy during restore (default: False)
                    skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        _subclient_object = self._get_subclient()
        restore_job = _subclient_object.in_place_restore_onedrive_v2(users, **kwargs)
        return restore_job

    def out_of_place_restore(self, users, destination_path, **kwargs):
        """ Run an out-of-place restore of specified users for OneDrive for business client

            Args:
                users (list) : list of SMTP addresses of users
                destination_path (str) : SMTP address of destination user
                **kwargs (dict) : Additional parameters
                    overwrite (bool) : unconditional overwrite files during restore (default: False)
                    restore_as_copy (bool) : restore files as copy during restore (default: False)
                    skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        _subclient_object = self._get_subclient()
        restore_job = _subclient_object.out_of_place_restore_onedrive_v2(users, destination_path, **kwargs)
        return restore_job

    def disk_restore(self,
                     users,
                     destination_client,
                     destination_path,
                     skip_file_permissions=False):
        """ Runs disk restore of specified users for OneDrive for business client

               Args:
                users (list) : list of SMTP addresses of users
                destination_client (str) : client where the users need to be restored
                destination_path (str) : Destination folder location
                skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        _subclient_object = self._get_subclient()
        restore_job = _subclient_object.disk_restore_onedrive_v2(users,
                                                        destination_client,
                                                        destination_path,
                                                        skip_file_permissions=skip_file_permissions)
        return restore_job

    def modify_server_plan(self,old_plan,new_plan):
        """
           Method to Modify Server Plan Associated to Client

           Arguments:
                old_plan        (str)   --     existing server plan name
                new_plan        (str)   --     new server plan name
        """

        from ..plan import Plan
        entities=[{
            "clientName" : self.client_name
        }]
        self.plan_obj = Plan(self._commcell_object, old_plan)
        self.plan_obj.edit_association(entities, new_plan)


    def modify_job_results_directory(self,modified_shared_jr_directory):
        """
        Method to modify job results directory

        modified_shared_jr_directory  (str)   --     new job results directory
        """
        jr_update_dict={
                "client": {
                    "jobResulsDir": {
                        "path": modified_shared_jr_directory
                    }
                }
        }

        self.update_properties(properties_dict=jr_update_dict)
