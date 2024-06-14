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
Module for operating with index server subclient

IndexServerSubClient is the only class defined in this file

IndexServerSubClient :    Derived class from BigDataAppsSubclient Base class, representing
Index Server subclient and to perform operations on that subclient

IndexServerSubClient:
===============

     __init__                           --  initialise object of the IndexServerSubClient class

    run_backup                          --  run backup job for this index server

    configure_backup                    --  Edit default subclient on index server for modifying subclient role content

    do_restore_in_place                 --  restores the index server index to index server client

    do_restore_out_of_place             --  restores the index server index to the specified dir on client

    get_file_details_from_backup        --  gets folder/file details from index server backup using index find

    _get_path_for_restore               --  forms path argument for restore based on index server mode

"""

from ..exception import SDKException
from ..index_server import IndexServerOSType
from ..subclients.bigdataappssubclient import BigDataAppsSubclient


class IndexServerSubclient(BigDataAppsSubclient):
    """
    Derived class from BigDataAppsSubclient, representing index server subclient,
    and to perform operations on that subclient
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Constructor for the IndexServerSubclient class

        Args:
            backupset_object  (object)  -- instance of the Backupset class

            subclient_name    (str)     -- name of the subclient

            subclient_id      (str)     -- id of the subclient

        """
        super(
            IndexServerSubclient,
            self).__init__(backupset_object, subclient_name, subclient_id)
        self._agent_object = self._backupset_object._agent_object
        self._instance_obj = self._backupset_object._instance_object
        self._client_object = self._agent_object._client_object
        self._commcell_object = self._backupset_object._commcell_object
        self._index_server_obj = self._commcell_object.index_servers.get(self._client_object.client_name)
        self._restore_options = {
            "destination_instance_id": self._instance_obj.instance_id,
            "multinode_restore": True,
            "client_type": 29
        }

    def _get_path_for_restore(self, roles=None, core_name=None, client=None):
        """ Forms the path argument for restore request based on specified input
 
        Args:
 
            roles       (list)      -- list of role names which needs to be restored
 
            core_name   (list)      -- list of solr core name which needs to be restored
 
            client      (str)       -- name of solr node client in case of solr cloud
                    ***Applicable only for solr cloud or CVSolr***
 
        Returns:
 
                list        --  list containing formatted paths
 
        Raises:
 
            SDKException:
 
                    if client name is not passed for index server cloud
 
                    if client is not a part of cloud
 
        """
        paths = []
        if client is None:
            client = self._index_server_obj.client_name[0]
        if client not in self._index_server_obj.client_name:
            raise SDKException('IndexServers', '104', 'Given client name is not part of index server cloud')
 
        path_delimiter = "\\"
        if self._index_server_obj.os_type == IndexServerOSType.UNIX.value:
            path_delimiter = "/"
 
        if core_name is None and roles is not None:
            paths = [f"{path_delimiter}{role}{path_delimiter}{client}" for role in roles]
 
        elif roles is None and core_name is not None:
            for core in core_name:
                core = core.replace(path_delimiter, f"{path_delimiter}{client}{path_delimiter}")
                paths.append(f"{path_delimiter}{core}")
 
        elif len(roles) == 1 and core_name is not None:
            for core in core_name:
                paths.append(f"{path_delimiter}{roles[0]}{path_delimiter}{client}{path_delimiter}{core}")
 
        else:
            for role in self.content:
                role = role.replace("\\", '')
                role = role.replace("%", '')
                paths.append(f"{path_delimiter}{role}{path_delimiter}{client}")
 
        return paths

    def do_restore_in_place(
            self,
            roles=None,
            core_name=None,
            overwrite=True,
            from_time=None,
            to_time=None,
            client=None):
        """Restores the indexed data for the specified role or core list to the same index location on index server

            Args:
                roles                   (list)  --  list of role name to be restored
                    default:None (all roles defined in this subclient)
                        Example : ['Data Analytics']

                core_name               (list)  --  list of solr core name which needs to be restore.
                    default:None (all cores)
                            Format : [role name/core name]
                            Example : ['Data Analytics\\cvcorefla0']

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                client          (str)           --  name of solr client whose data needs to be restored.**
                        ***Applicable only for solr cloud mode***
                        default : None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        paths = self._get_path_for_restore(roles=roles, core_name=core_name, client=client)
        proxy_client = self._index_server_obj.client_name[0]
        if self._index_server_obj.is_cloud or len(self._index_server_obj.client_name) > 1:
            proxy_client = client

        job_obj = self.restore_in_place(paths=paths, overwrite=overwrite,
                                        from_time=from_time, to_time=to_time,
                                        proxy_client=proxy_client,
                                        fs_options=self._restore_options)
        return job_obj

    def do_restore_out_of_place(
            self,
            dest_client,
            dest_path,
            roles=None,
            core_name=None,
            overwrite=True,
            from_time=None,
            to_time=None,
            client=None):
        """Restores the indexed data for the specified role or core list to any other client

            Args:

                dest_client             (str)   -- Client where index needs to be restored

                dest_path               (str)   -- folder path where index needs to be restored on client

                roles                   (list)  --  list of role name to be restored
                    default:None (all roles defined in this subclient)
                        Example : ['Data Analytics']

                core_name               (list)  --  list of solr core name which needs to be restore.
                    default:None (all cores)
                            Format : [role name/core name]
                            Example : ['Data Analytics\\cvcorefla0']

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                client          (str)           --  name of Index server client whose data needs to be restored.**
                        ***Applicable only for solr cloud mode***
                        default : None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if input data type is not valid

                    if failed to initialize job

        """
        if not isinstance(dest_path, str) or not isinstance(dest_client, str):
            raise SDKException('IndexServers', '101')

        paths = self._get_path_for_restore(roles=roles, core_name=core_name, client=client)
        job_obj = self.restore_out_of_place(client=dest_client, destination_path=dest_path,
                                            paths=paths, to_time=to_time, from_time=from_time,
                                            overwrite=overwrite,
                                            fs_options=self._restore_options)
        return job_obj

    def run_backup(self, backup_level="Full"):
        """Runs a backup job for the default subclient.

                    Args:
                        backup_level        (str)   --  level of backup the user wish to run
                            default: Full

                    Returns:
                        object - instance of the Job class for this backup job

                    Raises:
                        SDKException:
                            if backup level specified is not correct

                            if failed to start job
        """
        backup_level = backup_level.lower()
        # we support only full as of now
        if backup_level not in ['full']:
            raise SDKException('IndexServers', '105')
        if not (self.is_backup_enabled or self._client_object.is_backup_enabled):
            raise SDKException('IndexServers', '107')

        if self.storage_policy is None:
            raise SDKException('IndexServers', '106')
        job_obj = self.backup(backup_level=backup_level)
        return job_obj

    def get_file_details_from_backup(self, roles=None, include_files=True, job_id=0, index_server_node=None,
                                     **kwargs):
        """Gets files/folders details from index server backup job.

                    Args:

                        roles               (list)  --  list of roles whose file details needs to be fetched from backup

                        include_files       (bool)  --  whether to include files in response or not
                            default : True (Both files/folders from backup will be returned)
                            Note : Works only in the case of Windows IS, does not work for Linux IS

                        job_id              (str)   --  job id to be used for browse

                        index_server_node   (str)   --  index server client node name
                            Note : Required compulsory in the case of unix IS when roles is not none.

                        kwargs                      --  Additional info
                            ex -> core_list (list)  --  List of cores whose file details needs to be fetched
                                                             from backup


                     Returns: (list, dict)

                        list    -   List of only the file, folder paths from the browse response

                        dict    -   Dictionary of all the paths with additional metadata retrieved
                                    from browse operation

                    Raises:
                        SDKException:

                            if failed to do browse
        """

        find_options = {}
        if roles is None:
            find_options['path'] = '\\**\\*'
            if self._index_server_obj.os_type == IndexServerOSType.UNIX.value:
                find_options['path'] = '/**/*'

        else:
            roles_path = [f"\\{role}\\**\\*" for role in roles]
            if index_server_node is not None:
                roles_path = [f"\\{role}\\{index_server_node}\\**\\*" for role in roles]

            if self._index_server_obj.os_type == IndexServerOSType.UNIX.value:
                if index_server_node is None:
                    raise SDKException('IndexServers', '109')
                if len(roles) > 1:
                    raise SDKException('IndexServers', '110')

                roles_path = [f"/{roles[0]}/{index_server_node}"]
                
                core_list = kwargs.get('core_list')
                if core_list is not None:
                    roles_path = [f"/{roles[0]}/{index_server_node}/{core}" for core in core_list]

                find_options['operation'] = 'browse'

            find_options['path'] = roles_path
        if job_id != 0:
            find_options['job_id'] = job_id
        if include_files:
            find_options['include_meta_data'] = True
        else:
            find_options['hide_user_hidden'] = True

        return self.find(find_options)

    def configure_backup(self, storage_policy, role_content):
        """Edit the default subclient for modifying role content or storage policy.

                    Args:

                        storage_policy      (str)   --  Storage policy to be associated with default subclient

                        role_content        (list)  --  list of role names which needs to be backed up

                    Returns:

                        None

                    Raises:
                        SDKException:

                                if input data type is not valid

                                if response is empty

                                if response is not success
        """

        if not isinstance(storage_policy, str):
            raise SDKException('IndexServers', '101')
        if not isinstance(role_content, list):
            raise SDKException('IndexServers', '101')

        append_str = "%"
        delimiter = "/"
        role_content = [f"{delimiter}{append_str}{role}{append_str}" for role in role_content]
        self.content = role_content
        if self.storage_policy is None:
            self.storage_policy = storage_policy
        elif self.storage_policy.lower() != storage_policy.lower():
            self.storage_policy = storage_policy
