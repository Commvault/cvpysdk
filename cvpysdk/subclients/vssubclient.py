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
    _get_subclient_content_()   --  gets the content of a virtual server subclient

    _set_subclient_content_()   --  sets the content of a virtual server subclient

    _get_vm_ids_dict()          --  creates a dictionary with VM id as key, and its name as value

    _process_browse_response()  --  processes the browse response received from server and replaces
                                        the vm id with the vm name

    browse()                    --  gets the content of the backup for this subclient
                                        at the vm path specified

    browse_in_time()            --  gets the content of the backup for this subclient
                                        at the input vm path in the time range specified

    guest_files_browse()        --  browses the Files and Folders inside a Virtual Machine

    guest_files_browse_in_time()--  browses the Files and Folders inside a Virtual Machine
                                        in the time range specified

    vm_files_browse()           --  browses the Files and Folders of a Virtual Machine

    vm_files_browse_in_time()   --  browses the Files and Folders of a Virtual Machine
                                        in the time range specified

    disk_level_browse()         --  browses the Disks of a Virtual Machine

    disk_level_browse_in_time() --  browses the Disks of a Virtual Machine
                                        in the time range specified

"""

from ..exception import SDKException
from ..subclient import Subclient


class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self, subclient_properties):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of subclient

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
            subclient_content = subclient_properties['vmContent']

            if 'children' in subclient_content:
                children = subclient_content['children']

                for child in children:
                    path = str(child['path']) if 'path' in child else None
                    display_name = str(child['displayName'])
                    content_type = content_types[str(child['type'])]
                    vm_id = str(child['name'])

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

    def _get_vm_ids_dict(self, vm_path):
        """Parses through the subclient content and creates a dictionary consisting of the
            VM id as the key, and its name as the value.

            Args:
                vm_path     (str)   --  vm path to browse, and get the contents of

            Returns:
                dict    -   dictionary consisting of VM ID as Key and VM Display Name as Value
                str     -   path to browse contents of
        """
        if vm_path in ['\\', '']:
            vm_ids = {}

            for content in self.content:
                vm_ids[content['id']] = content['display_name']
        else:
            vm_ids = {}
            if not vm_path.startswith('\\'):
                vm_path = '\\' + vm_path

            vm_path_list = vm_path.split('\\')

            vm_name = vm_path_list[1]

            for content in self.content:
                if content['display_name'] in vm_path_list[1]:
                    vm_path = vm_path.replace(vm_path_list[1], content['id'])
                    vm_ids[content['id']] = vm_name
                    break

        return vm_ids, vm_path

    def _process_browse_response(self, vm_ids, browse_content):
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
        vm_ids, vm_path = self._get_vm_ids_dict(vm_path)

        browse_content = super(VirtualServerSubclient, self).browse(
            vm_path, show_deleted_files, vm_disk_browse
        )

        return self._process_browse_response(vm_ids, browse_content)

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
                path                (str)   --  folder path to get the contents of
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
        vm_ids, vm_path = self._get_vm_ids_dict(vm_path)

        browse_content = super(VirtualServerSubclient, self).browse_in_time(
            vm_path, show_deleted_files, restore_index, vm_disk_browse, from_date, to_date
        )

        return self._process_browse_response(vm_ids, browse_content)

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
                path                (str)   --  folder path to get the contents of
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
                path                (str)   --  folder path to get the contents of
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
                path                (str)   --  folder path to get the contents of
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
