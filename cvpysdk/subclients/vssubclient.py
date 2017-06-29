#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Subclient.

VirualServerSubclient is the only class defined in this file.

VirtualServerSubclient: Derived class from Subclient Base class, representing a
                            virtual server subclient, and to perform operations on that subclient

VirtualServerSubclient:
    _get_subclient_content_()       --  gets the content of a virtual server subclient

    _set_subclient_content_()       --  sets the content of a virtual server subclient

    _get_vm_ids_and_names_dict()    --  creates and returns 2 dictionaries, along with the vm path

    _parse_vm_path()                --  parses the path provided by user,
                                            and replaces the VM Display Name with the VM ID

    _process_vsa_browse_response()  --  processes the browse response received from server,
                                            and replaces the vm id with the vm name

    _process_restore_request()      --  processes the Restore Request and replaces the VM display
                                            name with their ID before passing to the API

    browse()                        --  gets the content of the backup for this subclient
                                            at the vm path specified

    browse_in_time()                --  gets the content of the backup for this subclient
                                            at the input vm path in the time range specified

    guest_files_browse()            --  browses the Files and Folders inside a Virtual Machine

    guest_files_browse_in_time()    --  browses the Files and Folders inside a Virtual Machine
                                            in the time range specified

    vm_files_browse()               --  browses the Files and Folders of a Virtual Machine

    vm_files_browse_in_time()       --  browses the Files and Folders of a Virtual Machine
                                            in the time range specified

    disk_level_browse()             --  browses the Disks of a Virtual Machine

    disk_level_browse_in_time()     --  browses the Disks of a Virtual Machine
                                            in the time range specified

    restore_out_of_place()          --  restores the VM Guest Files specified in the paths list
                                            to the client, at the specified destionation location

    full_vm_restore_in_place()      --  restores the VM specified by the user to the same location

"""

from __future__ import unicode_literals

import xmltodict

from past.builtins import basestring

from ..exception import SDKException
from ..subclient import Subclient


class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        content_types = {
            '1': 'Host',
            '2': 'Resource Pool',
            '4': 'Datacenter',
            '9': 'Virtual Machine',
            '16': 'All unprotected VMs',
            '17': 'Root'
        }

        if 'vmContent' in self._subclient_properties:
            subclient_content = self._subclient_properties['vmContent']

            if 'children' in subclient_content:
                children = subclient_content['children']

                for child in children:
                    path = child['path'] if 'path' in child else None
                    display_name = child['displayName']
                    content_type = content_types[child['type']]
                    vm_id = child['name']

                    temp_dict = {
                        'id': vm_id,
                        'path': path,
                        'display_name': display_name,
                        'type': content_type
                    }

                    content.append(temp_dict)

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Virtual Server Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        content_types = {
            'Host': '1',
            'Root': '17',
            'Datacenter': '4',
            'Resource Pool': '2',
            'Virtual Machine': '9',
            'All unprotected VMs': '16'
        }

        try:
            for temp_dict in subclient_content:
                virtual_server_dict = {
                    'allOrAnyChildren': True,
                    'equalsOrNotEquals': True,
                    'name': temp_dict['id'],
                    'displayName': temp_dict['display_name'],
                    'path': temp_dict['path'],
                    'type': content_types[temp_dict['type']]
                }

                content.append(virtual_server_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        vs_subclient_content = {
            "children": content
        }

        return vs_subclient_content

    def _get_vm_ids_and_names_dict(self):
        """Parses through the subclient content and creates 2 dictionaries.

            Returns:
                dict    -   dictionary consisting of VM ID as Key and VM Display Name as Value

                dict    -   dictionary consisting of VM Display Name as Key and VM ID as Value
        """
        vm_ids = {}
        vm_names = {}

        for content in self.content:
            vm_ids[content['id']] = content['display_name']
            vm_names[content['display_name']] = content['id']

        return vm_ids, vm_names

    def _parse_vm_path(self, vm_names, vm_path):
        """Parses the path provided by user, and replaces the VM Display Name with the VM ID.

            Returns:
                str     -   string of path to run browse for
        """
        if vm_path not in ['\\', '']:
            if not vm_path.startswith('\\'):
                vm_path = '\\' + vm_path

            vm_path_list = vm_path.split('\\')

            for vm_name in vm_names:
                if vm_name in vm_path_list[1]:
                    vm_path = vm_path.replace(vm_path_list[1], vm_names[vm_name])
                    break

        return vm_path

    def _process_vsa_browse_response(self, vm_ids, browse_content):
        """Processes the Browse response and replaces the VM ID with their display name before
            returning to user.

            Args:
                vm_ids          (dict)      --  dictionary with VM ID as Key and VM Name as Value

                browse_content  (tuple)     --  browse response received from server

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time
        """
        for index, path in enumerate(browse_content[0]):
            if vm_ids:
                for vm_id in vm_ids:
                    if vm_id in path:
                        browse_content[0][index] = path.replace(vm_id, vm_ids[vm_id])

        temp_dict = {}

        for path in browse_content[1]:
            if vm_ids:
                for vm_id in vm_ids:
                    if vm_id in path:
                        temp_dict[path.replace(vm_id, vm_ids[vm_id])] = browse_content[1][path]

        return browse_content[0], temp_dict

    def _process_restore_request(self, vm_names, restore_content):
        """Processes the Restore Request and replaces the VM display name with their ID before
            passing to the API.

            Args:
                vm_names            (dict)      --  dictionary with VM Name as Key, VM ID as Value

                restore_content     (tuple)    --  content to restore specified by user

            Returns:
                list - list of all folders or files with their full paths inside the input path
        """
        for index, path in enumerate(restore_content):
            if vm_names:
                for vm_name in vm_names:
                    if vm_name in path:
                        restore_content[index] = path.replace(vm_name, vm_names[vm_name])

        return restore_content

    def browse(self, vm_path='\\', show_deleted_files=True, vm_disk_browse=False):
        """Gets the content of the backup for this subclient at the path specified.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

                vm_disk_browse      (bool)  --  browse virtual machine files
                                                    e.g.; .vmdk files, etc.
                    only applicable when browsing content inside a guest virtual machine
                    default: False

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        vm_ids, vm_names = self._get_vm_ids_and_names_dict()

        vm_path = self._parse_vm_path(vm_names, vm_path)

        browse_content = super(VirtualServerSubclient, self).browse(
            vm_path, show_deleted_files, vm_disk_browse, True
        )

        return self._process_vsa_browse_response(vm_ids, browse_content)

    def browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            vm_disk_browse=False,
            from_date=None,
            to_date=None):
        """Gets the content of the backup for this subclient
            at the path specified in the time range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

                restore_index       (bool)  --  restore index if it is not cached
                    default: True

                from_date           (str)   --  date to get the contents after
                        format: dd/MM/YYYY

                        gets contents from 01/01/1970 if not specified
                    default: None

                to_date             (str)  --  date to get the contents before
                        format: dd/MM/YYYY

                        gets contents till current day if not specified
                    default: None

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if from date value is incorrect

                    if to date value is incorrect

                    if to date is less than from date

                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        vm_ids, vm_names = self._get_vm_ids_and_names_dict()

        vm_path = self._parse_vm_path(vm_names, vm_path)

        browse_content = super(VirtualServerSubclient, self).browse_in_time(
            vm_path, show_deleted_files, restore_index, vm_disk_browse, from_date, to_date, True
        )

        return self._process_vsa_browse_response(vm_ids, browse_content)

    def guest_files_browse(self, vm_path='\\', show_deleted_files=True):
        """Browses the Files and Folders inside a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        return self.browse(vm_path, show_deleted_files, False)

    def guest_files_browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            from_date=None,
            to_date=None):
        """Browses the Files and Folders inside a Virtual Machine in the time range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

                restore_index       (bool)  --  restore index if it is not cached
                    default: True

                from_date           (str)   --  date to get the contents after
                        format: dd/MM/YYYY

                        gets contents from 01/01/1970 if not specified
                    default: None

                to_date             (str)  --  date to get the contents before
                        format: dd/MM/YYYY

                        gets contents till current day if not specified
                    default: None

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if from date value is incorrect

                    if to date value is incorrect

                    if to date is less than from date

                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        return self.browse_in_time(
            vm_path, show_deleted_files, restore_index, False, from_date, to_date
        )

    def vm_files_browse(self, vm_path='\\', show_deleted_files=True):
        """Browses the Files and Folders of a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        return self.browse(vm_path, show_deleted_files, True)

    def vm_files_browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            from_date=None,
            to_date=None):
        """Browses the Files and Folders of a Virtual Machine in the time range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

                restore_index       (bool)  --  restore index if it is not cached
                    default: True

                from_date           (str)   --  date to get the contents after
                        format: dd/MM/YYYY

                        gets contents from 01/01/1970 if not specified
                    default: None

                to_date             (str)  --  date to get the contents before
                        format: dd/MM/YYYY

                        gets contents till current day if not specified
                    default: None

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if from date value is incorrect

                    if to date value is incorrect

                    if to date is less than from date

                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        return self.browse_in_time(
            vm_path, show_deleted_files, restore_index, True, from_date, to_date
        )

    def disk_level_browse(self, vm_path='\\', show_deleted_files=True):
        """Browses the Disks of a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        browse_content = self.browse(vm_path, show_deleted_files, True)

        paths_list = []

        for path in browse_content[0]:
            if path.endswith('.vmdk'):
                paths_list.append(path)

        paths_dict = {}

        for path in browse_content[1]:
            if path.endswith('.vmdk'):
                paths_dict[path] = browse_content[1][path]

        if paths_list and paths_dict:
            return paths_list, paths_dict
        else:
            return browse_content

    def disk_level_browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            from_date=None,
            to_date=None):
        """Browses the Disks of a Virtual Machine in the time range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

                restore_index       (bool)  --  restore index if it is not cached
                    default: True

                from_date           (str)   --  date to get the contents after
                        format: dd/MM/YYYY

                        gets contents from 01/01/1970 if not specified
                    default: None

                to_date             (str)  --  date to get the contents before
                        format: dd/MM/YYYY

                        gets contents till current day if not specified
                    default: None

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if from date value is incorrect

                    if to date value is incorrect

                    if to date is less than from date

                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        browse_content = self.browse_in_time(
            vm_path, show_deleted_files, restore_index, True, from_date, to_date
        )

        paths_list = []

        for path in browse_content[0]:
            if path.endswith('.vmdk'):
                paths_list.append(path)

        paths_dict = {}

        for path in browse_content[1]:
            if path.endswith('.vmdk'):
                paths_dict[path] = browse_content[1][path]

        if paths_list and paths_dict:
            return paths_list, paths_dict
        else:
            return browse_content

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True):
        """Restores the VM Guest files/folders specified in the input paths list to the client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                                                           the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                                                           files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files
                    default: True

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        from ..client import Client

        if not ((isinstance(client, basestring) or isinstance(client, Client)) and
                isinstance(destination_path, basestring) and
                isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if isinstance(client, Client):
            client = client
        elif isinstance(client, basestring):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        _, vm_names = self._get_vm_ids_and_names_dict()

        paths = self._process_restore_request(vm_names, paths)

        paths = self._filter_paths(paths)

        destination_path = self._filter_paths([destination_path], True)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            in_place=False,
            client=client,
            destination_path=destination_path,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl
        )

        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(
            self,
            vm_to_restore,
            new_name=None,
            overwrite=True,
            restore_data_and_acl=True):
        """Restores the Full Virtual Machine specified in the input paths list to the same location

            Args:
                vm_to_restore           (str)   --  name of the vm to restore

                new_name                (str)   --  new name to restore the vm with
                                                        restores with same name, if None
                    default: None

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if vms_to_restore is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        if not (isinstance(vm_to_restore, basestring) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        _, vm_names = self._get_vm_ids_and_names_dict()

        vms_to_restore = self._process_restore_request(vm_names, ['\\' + vm_to_restore])

        vms_to_restore = self._filter_paths(vms_to_restore)

        if vms_to_restore == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            in_place=False,
            paths=vms_to_restore,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl
        )

        browse_result = self.vm_files_browse()

        vs_metadata = browse_result[1]['\\' + vm_to_restore][-1]

        vm_id = vm_names[vm_to_restore]
        host = vs_metadata['esxHost']
        datastore = vs_metadata['datastore']
        resource_pool = vs_metadata['resourcePoolPath']
        nics = xmltodict.parse(vs_metadata['nics'])['IdxMetadata_VMNetworks']
        nics_list = []

        if 'nic' in nics:
            if isinstance(nics['nic'], list):
                for nic in nics['nic']:
                    nic_dict = {
                        "sourceNetwork": nic['@name'],
                        "destinationNetwork": nic['@name']
                    }

                    nics_list.append(nic_dict)
            elif isinstance(nics['nic'], dict):
                nic_dict = {
                    "sourceNetwork": nics['nic']['@name'],
                    "destinationNetwork": nics['nic']['@name']
                }

                nics_list.append(nic_dict)

        disks = self.disk_level_browse(vm_to_restore)[1]

        vm_disks = []

        for disk, data in disks.items():
            disk_dict = {
                "name": disk.split('\\')[-1],
                "Datastore": data[-1]['datastore']
            }

            vm_disks.append(disk_dict)

        request_json['taskInfo']["subTasks"][0]["options"][
            "restoreOptions"]['virtualServerRstOption'] = {
                "isDiskBrowse": True,
                "viewType": 0,
                "vCenterInstance": {
                    "clientName": self._backupset_object._instance_object.v_center_name,
                    "clientId": int(self._backupset_object._agent_object._client_object.client_id),
                    "applicationId": int(self._backupset_object._agent_object.agent_id),
                    "instanceId": int(self._backupset_object._instance_object.instance_id)
                },
                "diskLevelVMRestoreOption": {
                    "passUnconditionalOverride": False,
                    "useVcloudCredentials": True,
                    "diskOption": 0,
                    "powerOnVmAfterRestore": False,
                    "esxServerName": self._backupset_object._instance_object.v_center_name,
                    "transportMode": 0,
                    "restoreToDefaultHost": False,
                    "userPassword": {
                        "userName": self._backupset_object._instance_object.v_center_username
                    },
                    "advancedRestoreOptions": [
                        {
                            "addToFailoverCluster": False,
                            "esxHost": host,
                            "resourcePoolPath": resource_pool,
                            "newName": vm_to_restore if new_name is None else new_name,
                            "Datastore": datastore,
                            "name": vm_to_restore,
                            "guid": vm_id,
                            "disks": vm_disks,
                            "nics": nics_list
                        }
                    ]
                }
            }

        return self._process_restore_response(request_json)
