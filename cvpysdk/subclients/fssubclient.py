# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a File System Subclient

FileSystemSubclient is the only class defined in this file.

FileSystemSubclient: Derived class from Subclient Base class, representing a file system subclient,
                        and to perform operations on that subclient

FileSystemSubclient:

    _get_subclient_properties()         --  initializes the subclient related properties of the
    File System subclient

    _get_subclient_properties_json()    --  gets all the subclient related properties of the
    File System subclient

    _advanced_backup_options()          --  sets the advanced backup options

    content()                           --  update the content of the subclient

    filter_content()                    --  update the filter of the subclient

    exception_content()                 --  update the exception of the subclient

    scan_type()                         --  update the scan type of the subclient

    trueup_option()                     --  enable/disable trueup option of the subclient

    trueup_days()                       --  update trueup after **n** days value of the subclient

    find_all_versions()                 --  returns the dict containing list of all the backed up
    versions of specified file

    backup()                            --  run a backup job for the subclient

"""

from __future__ import unicode_literals

from past.builtins import basestring

from ..subclient import Subclient
from ..exception import SDKException


class FileSystemSubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient.
    """

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.

        """
        super(FileSystemSubclient, self)._get_subclient_properties()

        if 'impersonateUser' in self._subclient_properties:
            self._impersonateUser = self._subclient_properties['impersonateUser']

        if 'fsSubClientProp' in self._subclient_properties:
            self._fsSubClientProp = self._subclient_properties['fsSubClientProp']

        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "impersonateUser": self._impersonateUser,
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "fsSubClientProp": self._fsSubClientProp,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def _fs_subclient_prop(self):
        """Returns the JSON for the fsSubclientProp tag in the Subclient Properties JSON"""
        return self._fsSubClientProp

    @_fs_subclient_prop.setter
    def _fs_subclient_prop(self, value):
        """Update the values of fsSubclientProp JSON.

            Args:
                value   (dict)  --  dictionary consisting of the JSON attribute as the key
                and the new data as its value

            Raises:
                SDKException:
                    if value is not of type dict

        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        for key, value in value.items():
            self._fsSubClientProp[key] = value

        if 'enableOnePass' in self._fsSubClientProp:
            del self._fsSubClientProp['enableOnePass']

        if 'isTurboSubclient' in self._commonProperties:
            del self._commonProperties['isTurboSubclient']

    def _set_content(self,
                     content=None,
                     filter_content=None,
                     exception_content=None):
        """Sets the subclient content / filter / exception content.

            Args:
                content             (list)  --  list of subclient content

                filter_content      (list)  --  list of filter content

                exception_content   (list)  --  list of exception content

        """
        if content is None:
            content = self.content

        if filter_content is None:
            filter_content = self.filter_content

        if exception_content is None:
            exception_content = self.exception_content

        update_content = []
        for path in content:
            file_system_dict = {
                "path": path
            }
            update_content.append(file_system_dict)

        for path in filter_content:
            filter_dict = {
                "excludePath": path
            }
            update_content.append(filter_dict)

        for path in exception_content:
            exception_dict = {
                "includePath": path
            }
            update_content.append(exception_dict)

        self._set_subclient_properties("_content", update_content)

    def _advanced_backup_options(self, options):
        """Generates the advanced backup options dict

            Args:
                options     (dict)  --  advanced backup options that are to be included
                                            in the request

            Returns:
                (dict)  -   generated advanced options dict
        """
        final_dict = super(FileSystemSubclient, self)._advanced_backup_options(options)

        if 'on_demand_input' in options and options['on_demand_input'] is not None:
            final_dict['onDemandInputFile'] = options['on_demand_input']

        if 'directive_file' in options and options['directive_file'] is not None:
            final_dict['onDemandInputFile'] = options['directive_file']

        if 'adhoc_backup' in options and options['adhoc_backup'] is not None:
            final_dict['adHocBackup'] = options['adhoc_backup']

        if 'inline_bkp_cpy' in options or 'skip_catalog' in options:
            final_dict['dataOpt'] = {
                'createBackupCopyImmediately': options.get('inline_bkp_cpy', False),
                'skipCatalogPhaseForSnapBackup': options.get('skip_catalog', False)
            }

        if 'adhoc_backup_contents' in options and options['adhoc_backup_contents'] is not None:
            if not isinstance(options['adhoc_backup_contents'], list):
                raise SDKException('Subclient', '101')

            final_dict['adHocBkpContents'] = {
                'selectedAdHocPaths': options['adhoc_backup_contents']
            }

        return final_dict

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        for path in self._content:
            if 'path' in path:
                content.append(path["path"])

        return content

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            File System Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    @property
    def filter_content(self):
        """Treats the subclient filter content as a property of the Subclient class."""
        _filter_content = []

        for path in self._content:
            if 'excludePath' in path:
                _filter_content.append(path["excludePath"])

        return _filter_content

    @filter_content.setter
    def filter_content(self, value):
        """Sets the filter content of the subclient as the value provided as input.

            example: ['*book*', 'file**']

            Raises:
                SDKException:
                    if failed to update filter content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if isinstance(value, list) and value != []:
            self._set_content(filter_content=value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient filter content should be a list value and not empty'
            )

    @property
    def exception_content(self):
        """Treats the subclient exception content as a property of the Subclient class."""
        _exception_content = []

        for path in self._content:
            if 'includePath' in path:
                _exception_content.append(path["includePath"])

        return _exception_content

    @exception_content.setter
    def exception_content(self, value):
        """Sets the exception content of the subclient as the value provided as input.

            example: ['*book*', 'file**']

            Raises:
                SDKException:
                    if failed to update exception content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if isinstance(value, list) and value != []:
            self._set_content(exception_content=value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                'Subclient exception content should be a list value and not empty'
            )

    @property
    def scan_type(self):
        """Gets the appropriate scan type for this Subclient

            Returns:
                int
                    1   -   Recursive Scan
                    2   -   Optimized Scan
                    3   -   Change Journal Scan

        """
        return self._fsSubClientProp['scanOption']

    @scan_type.setter
    def scan_type(self, scan_type_value):
        """Creates the JSON with the specified scan type to pass to the API
            to update the scan type of this File System Subclient.

            Args:
                scan_type_value     (int)   --  scan type value as indicated below

                    1   -   Recursive Scan
                    2   -   Optimized Scan
                    3   -   Change Journal Scan

            Raises:
                SDKException:
                    if failed to update scan type of subclient

                    if scan_type_value is invalid

        """
        if isinstance(scan_type_value, int) and scan_type_value >= 1 and scan_type_value <= 3:
            self._set_subclient_properties("_fsSubClientProp['scanOption']", scan_type_value)
        else:
            raise SDKException('Subclient', '102', 'Invalid scan type')

    @property
    def trueup_option(self):
        """Gets the value of TrueUp Option

            Returns:
                True    -   if trueup is enabled on the subclient

                False   -   if trueup is not enabled on the subclient

        """

        return self._fsSubClientProp['isTrueUpOptionEnabledForFS']

    @trueup_option.setter
    def trueup_option(self, trueup_option_value):
        """Creates the JSON with the specified scan type to pass to the API
            to update the scan type of this File System Subclient.

            Args:
                trueup_option_value (bool)  --  Specifies to enable or disable trueup
        """

        self._set_subclient_properties(
            "_fsSubClientProp['isTrueUpOptionEnabledForFS']",
            trueup_option_value
        )

    @property
    def trueup_days(self):
        """Gets the trueup after n days value for this Subclient

            Returns: int
        """

        return self._fsSubClientProp['runTrueUpJobAfterDaysForFS']

    @trueup_days.setter
    def trueup_days(self, trueup_days_value):
        """Creates the JSON with the specified trueup days to pass to the API
            to update the trueup after **n** days value of this File System Subclient.

            Args:
                trueup_days_value   (int)   --  run trueup after days

            Raises:
                SDKException:
                    if failed to update trueup after n days of subclient

                    if trueup_days_value is invalid

        """
        if isinstance(trueup_days_value, int):
            self._set_subclient_properties(
                "_fsSubClientProp['runTrueUpJobAfterDaysForFS']",
                trueup_days_value
            )
        else:
            raise SDKException('Subclient', '102', 'Invalid trueup days')

    def find_all_versions(self, *args, **kwargs):
        """Searches the content of a Subclient.

            Args:
                Dictionary of browse options:
                    Example:
                        find_all_versions({
                            'path': 'c:\\hello',
                            'show_deleted': True,
                            'from_time': '2014-04-20 12:00:00',
                            'to_time': '2016-04-31 12:00:00'
                        })

                    (OR)

                Keyword argument of browse options:
                    Example:
                        find_all_versions(
                            path='c:\\hello.txt',
                            show_deleted=True,
                            to_time='2016-04-31 12:00:00'
                        )

                Refer self._default_browse_options for all the supported options

        Returns:
            dict    -   dictionary of the specified file with list of all the file versions and
                            additional metadata retrieved from browse
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'all_versions'

        return self._backupset_object._do_browse(options)

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               collect_metadata=False,
               on_demand_input=None,
               advanced_options=None,
               schedule_pattern=None):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential / Synthetic_full
                    default: Incremental

                incremental_backup  (bool)  --  run incremental backup
                        only applicable in case of Synthetic_full backup
                    default: False

                incremental_level   (str)   --  run incremental backup before/after synthetic full
                        BEFORE_SYNTH / AFTER_SYNTH

                        only applicable in case of Synthetic_full backup
                    default: BEFORE_SYNTH

                on_demand_input     (str)   --  input directive file location for on
                                                    demand subclient

                        only applicable in case of on demand subclient
                    default: None

                advacnced_options   (dict)  --  advanced backup options to be included while
                                                    making the request
                        default: None

                        options:
                            directive_file          :   path to the directive file
                            adhoc_backup            :   if set triggers the adhoc backup job
                            adhoc_backup_contents   :   sets the contents for adhoc backup
                            inline_backup_copy      :   to run backup copy immediately(inline)
                            skip_catalog            :   skip catalog for intellisnap operation

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success

        """
        if on_demand_input is not None:
            if not isinstance(on_demand_input, basestring):
                raise SDKException('Subclient', '101')

            if not self.is_on_demand_subclient:
                raise SDKException(
                    'Subclient', '102', 'On Demand backup is not supported for this subclient'
                )

            if not advanced_options:
                advanced_options = {}

            advanced_options['on_demand_input'] = on_demand_input

        if advanced_options or schedule_pattern:
            request_json = self._backup_json(
                backup_level,
                incremental_backup,
                incremental_level,
                advanced_options,
                schedule_pattern
            )

            backup_service = self._services['CREATE_TASK']

            flag, response = self._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

        else:
            return super(FileSystemSubclient, self).backup(
                backup_level=backup_level,
                incremental_backup=incremental_backup,
                incremental_level=incremental_level,
                collect_metadata=collect_metadata
            )

        return self._process_backup_response(flag, response)
