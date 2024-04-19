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

"""File for operating on a File System Subclient

FileSystemSubclient is the only class defined in this file.

FileSystemSubclient: Derived class from Subclient Base class, representing a file system subclient,
                        and to perform operations on that subclient

FileSystemSubclient:

    _get_subclient_properties()         --  initializes the subclient related properties of the
    File System subclient

    _get_subclient_properties_json()    --  gets all the subclient related properties of the
    File System subclient

    _common_backup_options()            --  Generates the advanced job options dict

    _advanced_backup_options()          --  sets the advanced backup options

    enable_content_indexing             --  Enables Content indexing and add the policy associations

    disable_content_indexing            --  Disables Content indexing and disassociate the CI policy

    find_all_versions()                 --  returns the dict containing list of all the backed up
                                            versions of specified file

    backup()                            --  run a backup job for the subclient

    run_backup_copy()                   --  Runs the backup copy job from Subclient

    restore_in_place()                  --  Restores the files/folders
                                            specified in the input paths list to the same location.

    restore_out_of_place()              --  Restores the files/folders specified in the input paths list
                                            to the input client, at the specified destionation location


FileSystemSubclient Instance Attributes:
=======================================

    **_fs_subclient_prop**                --  Returns the JSON for the fsSubclientProp tag in the Subclient 
                                              Properties JSON
                                             
    **content**                           --  update the content of the subclient

    **filter_content**                    --  update the filter of the subclient

    **exception_content**                 --  update the exception of the subclient

    **scan_type**                         --  update the scan type of the subclient

    **trueup_option**                     --  enable/disable trueup option of the subclient

    **backup_retention**                  --  enable/disable backup retention for the subclient

    **backup_retention_days**             --  set number of days for backup retention

    **archiver_retention**                --  enable/disable archiver_retention of the subclient.

    **archiver_retention_days**           --  set number of days for archiver retention

    **file_version**                      --  set version mode and no of version or days

    **disk_cleanup**                      --  enable/disable disk cleanup tab

    **disk_cleanup_rules**                --  update rules for disk_cleanup

    **backup_only_archiving_candidate**   --  enable or disable backup only candidate on the subclient

    **trueup_days**                       --  update trueup after **n** days value of the subclient

    **generate_signature_on_ibmi**        --  enable or disable signature generation on ibmi

    **backup_using_multiple_drives**      --  enable or disable VTL multiple drives for ibmi subclient.

    **pending_record_changes**            --  Updates the pending record changes value on ibmi subclient.

    **other_pending_changes**             --  Updates the other pending changes value on ibmi subclient.

    **object_level_backup**               --  enable or disable object level backup for ibmi subclient

    **global_filter_status**              --  returns the status whther to include global filters

    **enable_synclib**                    --  enable or disable SAVACT option for ibmi subclients.

    **software_compression**              --  The software compression setting's value for the subclient.

    **use_vss**                           --  The Use VSS setting's value for the subclient.
  
    **block_level_backup_option**         --  Enable/Disable Blocklevel Option on subclient

    **create_file_level_index_option**    --  Enable/Disable Metadata collection Option on subclient

    **system_state_option**               --  Enable/Disable System state option for the subclient

    **_dc_options_dict**                  --   Data Classification plan  Options

    **enable_dc_content_indexing**        -- Enable Dataclassification Indexing option.

    **onetouch_option**                   --  Enable/Disable One-Touch option for the subclient

    **onetouch_server**                   --  Provides the 1-touch server name

    **onetouch_server_directory**         --  Provides the 1-touch server directory
    
    **catalog_acl**                       --  To enable/disable ACL on the subclient

    **index_server**                      --  Sets/gets the index server client for the subclient

    **index_pruning_type**                --  Sets the index pruning type

    **index_pruning_days_retention**      --  Sets the number of days to be maintained in
                                              subclient index

    **index_pruning_cycles_retention**    --  Sets the number of cycles to be maintained in
                                              subclient index
	
    **ibmi_dr_config**                    --  Sets the subclient into one touch mode and adds ibmi DR parameters

    **backup_savf_file_data**             --  Sets the savf file data property for ibmi backup.

    **backup_spool_file_data**            --  Gets the value of spool file data on ibmi option for IBMi subclient

    **backup_queue_data**                 --  Gets the value of queue data data on ibmi option for IBMi subclient.

    **backup_private_authorities**        --  Gets the value of private authorities on ibmi option for IBMi subclient.

    **target_release**                    --  Gets the value of target and release on ibmi option for IBMi subclient.

    **save_access_path**                  --  Gets the value of save access path on ibmi option for IBMi subclient.

    **update_history**                    --  Updates the update history property value on ibmi subclient.

    **ibmi_compression**                  --  Gets the value of IBMi compression property on
                                                ibmi option for IBMi subclient.

    **save_while_active_option**          --  Set the save while active options for an IBMi subclient.



	**pre_post_commands**				  --  Sets the pre/post commands for the subclient.

	**backup_nodes**                      --  Sets backup nodes for FS Agent under Network Share clients.

	**impersonate_user**                  --  Impersonation information for the subclient.
    
    **plan**                              -- Set plan without/with overriding Plan's default content.


"""

from __future__ import unicode_literals
from base64 import b64encode

from ..client import Client
from ..subclient import Subclient
from ..exception import SDKException
from ..job import Job


def _nested_dict(source, update_dict):
    """
    This function recursively update the source dictionary with new values.

    Args:
         source   (dict)  --  Original dictionary

         update_dict   (dict)  --  The changes which are need to make

    Return:
        dict  --  modified source dictionary with updated values

    """
    for key, value in update_dict.items():
        if isinstance(value, dict) and value:
            source[key] = _nested_dict(source.get(key, {}), value)
        else:
            source[key] = value
    return source


class FileSystemSubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient.
    """

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.

        """
        super(FileSystemSubclient, self)._get_subclient_properties()
        self._impersonateUser={}
        if 'impersonateUser' in self._subclient_properties:
            self._impersonateUser = self._subclient_properties['impersonateUser']

        if 'fsSubClientProp' in self._subclient_properties:
            self._fsSubClientProp = self._subclient_properties['fsSubClientProp']

        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

        self._global_filter_status_dict = {
            'OFF': 0,
            'ON': 1,
            'USE CELL LEVEL POLICY': 2
        }

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
                    "fsContentOperationType": "OVERWRITE",
                    "fsExcludeFilterOperationType": "OVERWRITE" if not hasattr(self, '_fsExcludeFilterOperationType') else self._fsExcludeFilterOperationType,
                    "fsIncludeFilterOperationType": "OVERWRITE" if not hasattr(self, '_fsIncludeFilterOperationType') else self._fsIncludeFilterOperationType
                }
        }

        if 'isDDBSubclient' in self._fs_subclient_prop:
            if self._fs_subclient_prop['isDDBSubclient']:
                del subclient_json["subClientProperties"]["content"]
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

        _nested_dict(self._fsSubClientProp, value)

        if 'enableOnePass' in self._fsSubClientProp:
            del self._fsSubClientProp['enableOnePass']

        if 'isTurboSubclient' in self._commonProperties:
            del self._commonProperties['isTurboSubclient']

    def _set_content(self,
                     content=None,
                     filter_content=None,
                     exception_content=None):
        """Sets the subclient content / filter / exception content

            Args:
                content             (list)      --  list of subclient content

                filter_content      (list)      --  list of filter content

                exception_content   (list)      --  list of exception content
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
        self._fsExcludeFilterOperationType = "OVERWRITE"  # RESET THE OPERATION TYPE TO ITS DEFAULT
        self._fsIncludeFilterOperationType = "OVERWRITE"  # RESET THE OPERATION TYPE TO ITS DEFAULT


    def _common_backup_options(self, options):
        """
         Generates the advanced job options dict

            Args:
                options     (dict)  --  advanced job options that are to be included
                                            in the request

            Returns:
                (dict)  -   generated advanced options dict
        """
        final_dict = super(FileSystemSubclient, self)._common_backup_options(options)

        common_options = {
            "jobDescription": options.get('job_description', ""),
            "jobRetryOpts": {
                "killRunningJobWhenTotalRunningTimeExpires": options.get(
                    'kill_running_job_when_total_running_time_expires', False),
                "numberOfRetries": options.get('number_of_retries', 0),
                "enableNumberOfRetries": options.get('enable_number_of_retries', False),
                "runningTime": {
                    "enableTotalRunningTime": options.get('enable_total_running_time', False),
                    "totalRunningTime": options.get('total_running_time', 3600)
                }
            },
            "startUpOpts": {
                "startInSuspendedState": options.get('start_in_suspended_state', False),
                "useDefaultPriority": options.get('use_default_priority', True),
                "priority": options.get('priority', 166)
            }
        }

        return common_options

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
                'skipCatalogPhaseForSnapBackup': options.get('skip_catalog', False)}

        if 'adhoc_backup_contents' in options and options['adhoc_backup_contents'] is not None:
            if not isinstance(options['adhoc_backup_contents'], list):
                raise SDKException('Subclient', '101')

            final_dict['adHocBkpContents'] = {
                'selectedAdHocPaths': options['adhoc_backup_contents']
            }

        if 'use_multi_stream' in options and options['use_multi_stream']:

            multi_stream_opts = {
                'useMultiStream': options.get('use_multi_stream', False),
                'useMaximumStreams': options.get('use_maximum_streams', True),
                'maxNumberOfStreams': options.get('max_number_of_streams', 1)
            }

            if 'dataOpt' in final_dict and isinstance(final_dict['dataOpt'], dict):
                final_dict['dataOpt'].update(multi_stream_opts)
            else:
                final_dict['dataOpt'] = multi_stream_opts

        if 'start_new_media' in options and options['start_new_media']:

            media_opts = {
                'startNewMedia': options.get('start_new_media', False)
            }

            if 'mediaOpt' in final_dict and isinstance(final_dict['mediaOpt'], dict):
                final_dict['mediaOpt'].update(media_opts)
            else:
                final_dict['mediaOpt'] = media_opts
        
        if options.get('media_agent_name'):
            media_agent_name = options['media_agent_name']
            if not isinstance(media_agent_name, str):
                message = f"media_agent_name: Expected str, received {type(media_agent_name)}"
                raise SDKException('Subclient', '101', message)
            final_dict['dataPathOpt'] = {
                "mediaAgent": {
                    "mediaAgentName": media_agent_name
                }
            }

        return final_dict

    @property
    def _vlr_restore_options_dict(self):
        """ Constructs volume level Restore Dictionary"""

        physical_volume = 'PHYSICAL_VOLUME'
        vlr_options_dict = {
            "volumeRstOption": {
                "volumeLeveRestore": True,
                "volumeLevelRestoreType": physical_volume
            },
            "virtualServerRstOption": {
                "isDiskBrowse": False,
                "isVolumeBrowse": True,
                "isBlockLevelReplication": False
            }
        }
        return vlr_options_dict

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
                'Subclient',
                '102',
                'Subclient content should be a list value and not empty')

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
            An empty list will clear all filters.

            example: ['*book*', 'file**']

            Raises:
                SDKException:
                    if failed to update filter content of subclient

                    if the type of value input is not list

        """
        if isinstance(value, list):
            if value == []:
                value = self.filter_content
                self._fsExcludeFilterOperationType = "DELETE"
            self._set_content(filter_content=value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                'Subclient filter content should be a list value')

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
        if isinstance(value, list):
            if value == []:
                value = self.exception_content
                self._fsIncludeFilterOperationType = "DELETE"
            self._set_content(exception_content=value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                'Subclient exception content should be a list value and not empty')

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

    def run_backup_copy(self):
        """
        Runs the backup copy from Commcell for the given subclient

        Args:
                None

        Returns:
                object - instance of the Job class for this backup copy job
        Raises:
            SDKException:

                    if backup copy job failed

                    if response is empty

                    if response is not success
        """
        request_json = {
            "taskInfo": {
                "associations": [
                    {
                        "clientName": self._client_object._client_name,
                        "subclientName": self._subclient_name,
                        "backupsetName": self._backupset_object._backupset_name,
                        "storagePolicyName": self.storage_policy,
                        "_type_": 17,
                        "appName": self._agent_object._agent_name
                    }
                ],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 1,
                    "taskId": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4028
                        },
                        "options": {
                            "adminOpts": {
                                "snapToTapeOption": {
                                    "allowMaximum": True,
                                    "noofJobsToRun": 1
                                }
                            }
                        }
                    }
                ]
            }
        }

        backup_copy = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_copy, request_json)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Backup copy job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '118', o_str)
                else:
                    raise SDKException('Subclient', '118', 'Failed to run the backup copy job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def backup_retention(self):
        """return if backup retention is enabled or not

        Returns:
                True    -   if backup_retention is enabled for the subclient

                False   -   if backup_rentention is not enabled for the subclient

        """

        return self._fsSubClientProp['backupRetention']

    @backup_retention.setter
    def backup_retention(self, value):
        """Creates the JSON with the specified Boolean variable to pass to the API
            to update the backup_retention of this File System Subclient

        Args:
             value   (bool)  --  To enable or disable backup_retention.

        """

        if isinstance(value, bool):

            if value:
                new_value = {
                    'extendStoragePolicyRetention': True,
                    'backupRetention': True}
            else:
                new_value = {'backupRetention': False}
            self._set_subclient_properties("_fs_subclient_prop", new_value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                'argument should only be boolean')

    @property
    def block_level_backup_option(self):
        """Gets the block level option

            Returns:
                true - if blocklevel is enabled on the subclient
                false - if blocklevel is not enabled on the subclient
        """

        return self._fsSubClientProp['blockLevelBackup']

    @block_level_backup_option.setter
    def block_level_backup_option(self, block_level_backup_value):
        """Creates the JSON with the specified blocklevel flag
            to pass to the API to update the blocklevel of this
            File System Subclient.

            Args:
                block_level_backup_value (bool)  --  Specifies to enable or disable blocklevel option
        """

        self._set_subclient_properties(
            "_fsSubClientProp['blockLevelBackup']",
            block_level_backup_value)


    @property
    def _dc_options_dict(self):
        """ Constructs Data classification Property"""
        dc_options = {'dcPlanEntity': {'planType': 7, 'planSubtype': 117506053, 'planName': ''}}
        return dc_options

    def enable_dc_content_indexing(self, dcplan_name):
        """Creates the JSON with the specified dataclassification plan to pass to API to
            update  file system Subclient

            Args:
                dcplan_name (String)  --  DC plan name

        """
        temp_dc = self._dc_options_dict
        temp_dc['dcPlanEntity']['planName'] = dcplan_name
        self.update_properties(temp_dc)

    @property
    def create_file_level_index_option(self):
        """Gets the value of Metadata collection Option

            Returns:
                true - if metadata collection is enabled on the subclient
                false - if metadata collection is not enabled on the subclient
        """

        return self._fsSubClientProp['createFileLevelIndexDuringBackup']

    @create_file_level_index_option.setter
    def create_file_level_index_option(self, create_file_level_index_value):
        """Creates the JSON with the specified scan type
            to pass to the API to update the Metadata collection of this
            File System Subclient.

            Args:
                create_file_level_index_value (bool)  --  Specifies to enable or disable metadata collection
        """

        self._set_subclient_properties(
            "_fsSubClientProp['createFileLevelIndexDuringBackup']",
            create_file_level_index_value)

    @property
    def backup_retention_days(self):
        """return number of days for backup retention

        Returns:
                        (int)

        """

        # For Indexing V2 clients
        if 'afterDeletionKeepItemsForNDays' in self._fsSubClientProp:
            return self._fsSubClientProp['afterDeletionKeepItemsForNDays']

        # For Indexing V1 clients
        else:
            return self._fsSubClientProp.get('daysToKeepItems', 0)

    @backup_retention_days.setter
    def backup_retention_days(self, value):
        """Creates the JSON with the specified backup_retention days to pass to the API
            to update the retention for deleted item of this File System Subclient

        Args:
                value   (int)  --  To set extended retention days for deleted items

                The value will be converted in years , months and days form on GUI.

                To set infinite ,value should be -1

        Raises:
                SDKException:
                    if failed to update days for deleted item retention for the subclient

                    if value is invalid

        """

        if isinstance(value, int):
            if 'afterDeletionKeepItemsForNDays' in self._fsSubClientProp:
                if value != -1:
                    new_value = {
                        'afterDeletionKeepItemsForNDays': value,
                        'backupRetentionMode': 1
                    }
                else:
                    new_value = {'afterDeletionKeepItemsForNDays': value}
            else:
                new_value = {
                    'daysToKeepItems': value
                }

            self._set_subclient_properties("_fs_subclient_prop", new_value)

        else:
            raise SDKException(
                'Subclient',
                '102',
                'argument should only be boolean')

    @property
    def system_state_option(self):
        """Checks whether the system state option is enabled

        Returns:
            True    -   if system state property is enabled for the subclient

            False   -   if system state property is not enabled for the subclient
        """
        return self._fsSubClientProp['backupSystemState']

    @system_state_option.setter
    def system_state_option(self, backup_system_state):
        """
        Enables the system state property for the subclient
        """
        self._set_subclient_properties(
            "_fsSubClientProp['backupSystemState']",
            backup_system_state)

    @property
    def onetouch_option(self):
        """Checks whether the onetouch option is enabled

        Returns:
            True    -   if system state property is enabled for the subclient

            False   -   if system state property is not enabled for the subclient
        """
        return self._fsSubClientProp.get('oneTouchSubclient')

    @onetouch_option.setter
    def onetouch_option(self, backup_onetouch):
        """
        Enables the system state property for the subclient
        """
        self._set_subclient_properties("_fsSubClientProp['oneTouchSubclient']", backup_onetouch)

    @property
    def onetouch_server(self):
        """
        Returns: Onetouch Server Name
        """
        return self._fsSubClientProp.get('oneTouchServer', {}).get('clientName')

    @onetouch_server.setter
    def onetouch_server(self, onetouch_server):
        """
        Sets the onetouch server property
        """
        self._set_subclient_properties(
            "_fsSubClientProp['oneTouchServer']['clientName']",
            onetouch_server)

    @property
    def onetouch_server_directory(self):
        """
        Returns the onetouch server directory
        """
        return self._fsSubClientProp.get('oneTouchServerDirectory')

    @onetouch_server_directory.setter
    def onetouch_server_directory(self, onetouch_server_directory):
        """
        Sets the onetouch server directory
        """
        self._set_subclient_properties(
            "_fsSubClientProp['oneTouchServerDirectory']",
            onetouch_server_directory)

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

    @property
    def archiver_retention(self):
        """return the value of archiver retention or modified time retention

          Returns:
                True    -   if archiver or modified time retention is enabled for the subclient

                False   -   if archiver or modified time retention is not enabled for the subclient


        """

        return self._fsSubClientProp['archiverRetention']

    @archiver_retention.setter
    def archiver_retention(self, value):
        """
        Creates the JSON with the specified Boolean variable to pass to the API
            to update the archiver or modified time based retention of this File System Subclient

        If archiver retention is enabled-
                With backup retention, the object based retention is selected and
                modified time based retention is selected.

                Without backup retention, job based retention is selected
        Args:
            value  (bool)  --  To enable or disable job based retention or modified time retention



        """
        if isinstance(value, bool):

            if value:
                new_value = {
                    'extendStoragePolicyRetention': True,
                    'archiverRetention': True}
            else:
                new_value = {'archiverRetention': False}
            self._set_subclient_properties("_fs_subclient_prop", new_value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                'argument should only be boolean')

    @property
    def archiver_retention_days(self):
        """return number of days for archiver or modified time  retention

           Return:
                                (int)
        """

        return self._fsSubClientProp['extendRetentionForNDays']

    @archiver_retention_days.setter
    def archiver_retention_days(self, value):
        """
        Creates the JSON with the specified archiver retention or modified time based retentiondays
         to pass to the API to update the respected value of this File System Subclient

        Args:
                value  (int)  --   To update archiving retention or modified time based retention

                               The value will be converted in years , months and days from on GUI.

                               To set infinite value should be -1

        Raises:
                SDKException:
                    if failed to update archiver retention days of subclient

                    if value is invalid


        """
        if isinstance(value, int):
            if value != -1:
                new_value = {
                    'extendRetentionForNDays': value,
                    'archiverRetentionMode': 1}
            else:
                new_value = {'extendRetentionForNDays': value}
            self._set_subclient_properties("_fs_subclient_prop", new_value)

        else:
            raise SDKException(
                'Subclient',
                '102',
                'argument should only be integer')

    @property
    def disk_cleanup(self):
        """
        return value of disk cleanup of the subclient

         Returns:
                True    -   if disk Cleanup is enabled for the subclient

                False   -   if disk Cleanup is not enabled for the subclient


        """
        diskcleanup = None
        if 'enableArchivingWithRules' in self._fsSubClientProp['diskCleanupRules']:
            return self._fsSubClientProp['diskCleanupRules']['enableArchivingWithRules']

        return diskcleanup

    @disk_cleanup.setter
    def disk_cleanup(self, value):
        """
        Creates the JSON with the specified Boolean to pass to the API
            to update the disk cleanup option of this File System Subclient

        Args:
            value   (bool)  --  To enable or disbale disk cleanup

        Raises:
                SDKException:
                    if failed to update the propety of subclient

                    if value is invalid

        """

        if isinstance(value, bool):

            self._set_subclient_properties(
                "_fsSubClientProp['diskCleanupRules']['enableArchivingWithRules']", value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                'argument should only be boolean')

    @property
    def disk_cleanup_rules(self):
        """
        return disk cleanup rules for this FileSystem Subclient

        Return:
            (dict)  --  disk clean up rules
        """

        return self._fsSubClientProp['diskCleanupRules']

    @disk_cleanup_rules.setter
    def disk_cleanup_rules(self, rules):
        """
        Creates the JSON with the specified dictionary value to pass to the API
            to update the disk cleanup rules of this File System Subclient

        Args:
                        rules   (dict)  --  To update the rules Only need to send the value which need to be
                        updated

                        {
                'useNativeSnapshotToPreserveFileAccessTime': False,
                'fileModifiedTimeOlderThan': 0,
                'fileSizeGreaterThan': 1024,
                'stubPruningOptions': 0, 0 to disable and 1,2 ,3 for different option

                'afterArchivingRule': 1, - 1 for stub the file and 2 for delete the file

                'stubRetentionDaysOld': 365,
                'fileCreatedTimeOlderThan': 0,
                'maximumFileSize': 0,
                'fileAccessTimeOlderThan': 89,
                'startCleaningIfLessThan': 50,
                'enableRedundancyForDataBackedup': True,
                 'stopCleaningIfupto': 80,

                 'diskCleanupFileTypes': {'fileTypes': ["%Text%", '%Image%']}

                 or

                 'diskCleanupFilesTypes':{} for no extension
                }
        Raises:
                SDKException:
                    if failed to update the property of the subclient

                    if value is invalid


        """
        if isinstance(rules, dict):
            value = {'diskCleanupRules': rules}
            self._set_subclient_properties("_fs_subclient_prop", value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                "The parameter should be dictionary")

    @property
    def backup_only_archiving_candidate(self):
        """
            To get the value of backup only archiving candidate

        Returns:
                True    -   if backup only archiving candidate is enabled for the subclient

                False   -   if backup only archiving candidate is not enabled for the subclient
        """
        return self._fsSubClientProp['backupFilesQualifiedForArchive']

    @backup_only_archiving_candidate.setter
    def backup_only_archiving_candidate(self, value):
        """
        Creates the JSON with the specified boolean value to pass to the API
            to update the backup only archiving candidate of this File System Subclient

        Args:
            value   (bool)  --  Enable or disable the option

        Raises:
                SDKException:
                    if failed to update the propety of subclient

                    if value is invalid

        """
        if isinstance(value, bool):
            self._set_subclient_properties(
                "_fsSubClientProp['backupFilesQualifiedForArchive']", value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                'The parameter must be boolean type')

    @property
    def file_version(self):
        """

        Returns:
                        (dict)  --  file version mode
        """
        version = {}

        # For Indexing V1 client, this property is not supported. Taking default versions by number
        if 'olderFileVersionsMode' not in self._fsSubClientProp:
            return {
                'Mode': 2,
                'DaysOrNumber': self._fsSubClientProp.get('keepAtLeastPreviousVersions', 0)
            }

        version['Mode'] = self._fsSubClientProp['olderFileVersionsMode']
        modes = {
            1: self._fsSubClientProp['keepOlderVersionsForNDays'],
            2: self._fsSubClientProp['keepVersions']
        }
        version['DaysOrNumber'] = modes.get(version['Mode'])
        return version

    @file_version.setter
    def file_version(self, value):
        """
            Creates the JSON with the specified dictionary to pass to the API
            to update the version mode and the value of this File System Subclient

        Args:
             value   (dict)  --  format -{'Mode':value,'DaysOrNumber':value}

                    Mode value 1- version based on modified time

                                2- No of version

                Example-
                    To set version based on modified time to 2 years

                    value={'Mode':1,'DaysOrNumber',730}

                    To set Number of version to 10

                    value={'Mode':2,'DaysOrNumber':10}
        Raises:
               SDKException:
                    if failed to update the propety of subclient

                    if value is invalid

        """

        if isinstance(value, dict):
            # For Indexing V2 client
            if 'olderFileVersionsMode' in self._fsSubClientProp:
                if value['Mode'] == 1 or value['Mode'] == 2:
                    new_value = {'olderFileVersionsMode': value['Mode']}
                else:
                    raise SDKException(
                        'Subclient', '102', "File version mode can only be 1 or 2")
                modes = {
                    1: 'keepOlderVersionsForNDays',
                    2: 'keepVersions'
                }

                new_value[modes[value['Mode']]] = value['DaysOrNumber']

            # For Indexing V1 client
            else:
                new_value = {
                    'keepAtLeastPreviousVersions': value['DaysOrNumber']
                }

            self._set_subclient_properties("_fs_subclient_prop", new_value)
        else:
            raise SDKException(
                'Subclient',
                '102',
                "Parameter need to be dictionary")

    @property
    def generate_signature_on_ibmi(self):
        """Gets the value of generate signature on ibmi option for IBMi subclient.

            Returns:
                False   -   if signature generation on IBMi is enabled on the subclient

                True    -   if signature generation on IBMi is not enabled on the subclient
        """
        return bool(self._fsSubClientProp.get('genSignatureOnIBMi'))

    @generate_signature_on_ibmi.setter
    def generate_signature_on_ibmi(self, generate_signature_value):
        """Updates the generate signature property value on ibmi subclient.

            Args:
                generate_signature_value (int)  --  Enable or disable signature generation on IBMi
        """
        self._set_subclient_properties(
            "_fsSubClientProp['genSignatureOnIBMi']",
            generate_signature_value
        )

    @property
    def backup_using_multiple_drives(self):
        """Gets the value of VTL multiple drives on ibmi option for IBMi subclient.

            Returns:
                False   -   if multiple drives is not enabled.

                True    -   if multiple drives is enabled.
        """
        return bool(self._fsSubClientProp.get('backupUsingMultipleDrives',False))

    @backup_using_multiple_drives.setter
    def backup_using_multiple_drives(self, set_vtl_multiple_drives):
        """Updates the VTL multiple drives property value on ibmi subclient.

            Args:
                set_vtl_multiple_drives (bool)  --  Enable or disable VTL multiple drives on IBMi
        """
        update_properties = self.properties
        if isinstance(set_vtl_multiple_drives, bool):
            update_properties['fsSubClientProp']['backupUsingMultipleDrives'] = set_vtl_multiple_drives
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)
    
    @property
    def pending_record_changes(self):
        """Gets the value of pending record changes option for  IBMi subclient.

            Returns:
                False   -   if multiple drives is not enabled.

                True    -   if multiple drives is enabled.
        """
        return bool(self._fsSubClientProp.get('pendingRecordChange'))

    @pending_record_changes.setter
    def pending_record_changes(self, value):
        """Updates the pending record changes value on ibmi subclient.

            Args:
                value   (str)  --  To set pending records changes value for backup data.
        """
        update_properties = self.properties
        if isinstance(value, str):
            update_properties['fsSubClientProp']['pendingRecordChange'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def other_pending_changes(self):
        """Gets the value of other pending changes for IBMi subclient.

            Returns:
                False   -   if multiple drives is not enabled.

                True    -   if multiple drives is enabled.
        """
        return bool(self._fsSubClientProp.get('otherPendingChange'))

    @other_pending_changes.setter
    def other_pending_changes(self, value):
        """Updates the other pending changes value on ibmi subclient.

            Args:
                value   (str)  --  To set other pending changes value for backup data.
        """
        update_properties = self.properties
        if isinstance(value, str):
            update_properties['fsSubClientProp']['otherPendingChange'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def object_level_backup(self):
        """Gets the value of object level backup option for IBMi subclient.

            Returns:
                True    -   if object level backup is enabled on the subclient

                False   -   if object level backup is not enabled on the subclient
        """
        return self._fsSubClientProp.get('backupAsObjects')

    @object_level_backup.setter
    def object_level_backup(self, object_level_value):
        """Updates the object level backup property for an IBMi subclient.

            Args:
                object_level_value (bool)  --  Specifies to enable or disable object level backup on IBMi
        """
        self._set_subclient_properties(
            "_fsSubClientProp['backupAsObjects']",
            object_level_value
        )

    @property
    def global_filter_status(self):
        """Returns the status whether the global filters are included in configuration"""
        for key, value in self._global_filter_status_dict.items():
            if self._fsSubClientProp.get('useGlobalFilters') == value:
                return key

    @global_filter_status.setter
    def global_filter_status(self, value):
        """Sets the configuration flag whether to include global filters

            Accepted Values:
                1. `OFF`

                2. `ON`

                3. `USE CELL LEVEL POLICY`
        """
        if not isinstance(value, str):
            raise SDKException('Subclient', '101')

        return self._set_subclient_properties(
            "_fsSubClientProp['useGlobalFilters']", self._global_filter_status_dict.get(value, 2)
        )

    @property
    def enable_synclib(self):
        """
        Return the save while active options for an IBMi subclient.

        Returns:
             (dict) --  Dictionary of synclib options
        """
        return {
            'saveWhileActiveOpt': self._fsSubClientProp['saveWhileActiveOpt'],
            'syncQueue': self._fsSubClientProp['syncQueue'],
            'syncAllLibForBackup': self._fsSubClientProp['syncAllLibForBackup'],
            'txtlibSyncCheckPoint': self._fsSubClientProp['txtlibSyncCheckPoint'],
            'activeWaitTime': self._fsSubClientProp['activeWaitTime']
        }

    @enable_synclib.setter
    def enable_synclib(self, synclib_config):
        """
        Updates the save while active backup property for an IBMi subclient.

            Args:
                synclib_config      (dict)  -- Dictionary of synclib config options

                    options                 --

                        synclib_value       (str)   --  Value of save while active option.

                        sync_queue          (str)   --  Path for the sync queue

                        sync_all_lib        (bool)  --  Whether to synchronize all libraries.

                        check_point         (str)   --  Command to run on checkpoint

                        active_wait_time    (int)   --  Amount of time to wait for check point.

        Returns:
            None

        Raises:
            SDKException:
                if failed to update the property of the subclient

                if value is invalid
        """
        update_properties = self.properties
        if isinstance(synclib_config, dict):
            update_properties['fsSubClientProp'] = synclib_config
        else:
            raise SDKException('Subclient', '102', 'The parameter should be a dictionary.')
        self.update_properties(update_properties)

    @property
    def software_compression(self):
        """Returns the software compression status for this subclient.

            Returns:    int
                    1   -   On Client
                    2   -   On Media Agent
                    3   -   Use Storage Policy Settings
                    4   -   Off

        """
        return self._fsSubClientProp['commonProperties']['storageDevice']['softwareCompression']

    @software_compression.setter
    def software_compression(self, sw_compression_value):
        """Updates the software compression property for a subclient.

            Args:
                sw_compression_value  (int)   --  Specifies the software compression method indicated by values below.
                    1   -   On Client
                    2   -   On Media Agent
                    3   -   Use Storage Policy Settings
                    4   -   Off

            Raises:
                SDKException:
                    if failed to update software compression method of subclient

                    if software_compression_value is invalid
        """
        if isinstance(sw_compression_value, int) and sw_compression_value in range(1, 5):
            attr_name = "_commonProperties['storageDevice']['softwareCompression']"
            self._set_subclient_properties(attr_name, sw_compression_value)
        else:
            raise SDKException('Subclient', '102', 'Invalid value for software compression type.')

    @property
    def use_vss(self):
        """Returns the value of the Use VSS options for Windows FS subclients.

            Returns:    dict

                Dictionary contains the keys 'useVSS', 'vssOptions' and 'useVssForAllFilesOptions'.

                useVSS:
                    True    -   ENABLED
                    False   -   DISABLED

                vssOptions:
                    1   -   For all files
                    2   -   For locked files only

                useVssForAllFilesOptions:
                    1   -   Fail the job
                    2   -   Continue and reset access time
                    3   -   Continue and do not reset access time

        """
        return {"useVSS": self._fsSubClientProp['useVSS'],
                "vssOptions": self._fsSubClientProp['vssOptions'],
                "useVssForAllFilesOptions": self._fsSubClientProp['useVssForAllFilesOptions']}

    @use_vss.setter
    def use_vss(self, value):
        """Updates the value of the Use VSS options for Windows FS subclients.

            Args:
                value  (dict)   --  Specifies the value of the Use VSS options for Windows FS subclients.

                    useVSS:
                        True    -   ENABLED
                        False   -   DISABLED

                    vssOptions:
                        1   -   For all files
                        2   -   For locked files only

                    useVssForAllFilesOptions:
                        1   -   Fail the job
                        2   -   Continue and reset access time
                        3   -   Continue and do not reset access time

        """
        fs_subclient_prop = self._fs_subclient_prop

        if isinstance(value['useVSS'], bool):
            fs_subclient_prop['useVSS'] = value['useVSS']
        else:
            raise SDKException('Subclient', '101')

        if isinstance(value['useVssForAllFilesOptions'], int) and value['useVssForAllFilesOptions'] in range(1, 4):
            fs_subclient_prop['useVssForAllFilesOptions'] = value['useVssForAllFilesOptions']
        else:
            raise SDKException('Subclient', '101')

        if isinstance(value['vssOptions'], int) and value['vssOptions'] in range(1, 3):
            fs_subclient_prop['vssOptions'] = value['vssOptions']
        else:
            raise SDKException('Subclient', '101')

        self._set_subclient_properties('_fs_subclient_prop', fs_subclient_prop)

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
               schedule_pattern=None,
               common_backup_options=None):
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

                advanced_options    (dict)  --  advanced backup options to be included while
                                                    making the request
                        default: None

                        options:
                            directive_file          :   path to the directive file
                            adhoc_backup            :   if set triggers the adhoc backup job
                            adhoc_backup_contents   :   sets the contents for adhoc backup
                            inline_backup_copy      :   to run backup copy immediately(inline)
                            skip_catalog            :   skip catalog for intellisnap operation
                            start_new_media         :   enables the option to start new media for the job
                            media_agent_name        :   to run backup via this media agent
                            impersonate_gui         :   sets the initiatedFrom property to GUI if True

                common_backup_options      (dict)  --  advanced job options to be included while
                                                        making request

                        default: None

                        options:
                            job_description              :  job description to be set.

                            enable_number_of_retries     :  enables/disables the property, number of retrys.
                                values:
                                    True/False

                            number_of_retries            : total number of retries to be set.

                            enable_total_running_time    :  enables/disables the property, toal running time.
                                values:
                                    True/False

                            total_running_time           :  total run time to be set in (secs)

                            kill_running_job_when_total_running_time_expires    :   enables/disables the property.
                                values:
                                    True/False

                            start_in_suspended_state     :  enables/disables the property.
                                values:
                                    True/False

                            use_default_priority         :  enables/disables the property.
                                values:
                                    True/False

                            priority                     :  three digit number to be set.
                                default: 166

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

            Returns:
                object - instance of the Job class for this backup job if its an immediate Job
                         instance of the Schedule class for the backup job if its a scheduled Job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success

        """
        if on_demand_input is not None:
            if not isinstance(on_demand_input, str):
                raise SDKException('Subclient', '101')

            if not self.is_on_demand_subclient:
                raise SDKException(
                    'Subclient',
                    '102',
                    'On Demand backup is not supported for this subclient')

            if not advanced_options:
                advanced_options = {}

            advanced_options['on_demand_input'] = on_demand_input

        if advanced_options or schedule_pattern or common_backup_options:
            request_json = self._backup_json(
                backup_level,
                incremental_backup,
                incremental_level,
                advanced_options,
                schedule_pattern,
                common_backup_options
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

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None,
            proxy_client=None,
            advanced_options=None
    ):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up
                        validate_only       : To validate data backed up for restore


                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                proxy_client    (str)          -- Proxy client used during FS under NAS operations

                advanced_options    (dict)  -- Advanced restore options

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Returns:
                object - instance of the Job class for this restore job if its an immediate Job
                         instance of the Schedule class for this restore job if its a scheduled Job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        if fs_options is not None and fs_options.get('no_of_streams', 1) > 1 and not fs_options.get('destination_appTypeId', False):
            fs_options['destination_appTypeId'] = int(self._client_object.agents.all_agents.get('file system', self._client_object.agents.all_agents.get('windows file system', self._client_object.agents.all_agents.get('linux file system', self._client_object.agents.all_agents.get('big data apps', self._client_object.agents.all_agents.get('cloud apps', 0))))))
            if not fs_options['destination_appTypeId']:
                del fs_options['destination_appTypeId']

        return super(FileSystemSubclient, self).restore_in_place(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            schedule_pattern=schedule_pattern,
            proxy_client=proxy_client,
            advanced_options=advanced_options
        )

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None,
            advanced_options=None
    ):
        """Restores the files/folders specified in the input paths list to the input client,
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

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options

                    options:

                        preserve_level          : preserve level option to set in restore

                        proxy_client            : proxy that needed to be used for restore

                        impersonate_user        : Impersonate user options for restore

                        impersonate_password    : Impersonate password option for restore
                        in base64 encoded form

                        all_versions            : if set to True restores all the versions of the
                        specified file

                        versions                : list of version numbers to be backed up

                        media_agent             : Media Agent need to be used for Browse and restore

                        is_vlr_restore          : sets if the restore job is to be triggered as vlr

                        validate_only           : To validate data backed up for restore

                        instant_clone_options   : Options for FS clone found on Command Center, the value must be
                        a dictionary containing the following key value pairs.

                            reservation_time        (int)   --  The amount of time, specified in seconds, that the mounted
                            snapshot needs to be reserved for before it is cleaned up.
                            This is an OPTIONAL key.

                                Default :   3600

                            clone_mount_path        (str)   --  The path to which the snapshot needs to be mounted.
                            This is NOT an optional key.

                            post_clone_script       (str)   --  The script that will run post clone.
                            This is an OPTIONAL key.

                            clone_cleanup_script    (str)   --  The script that will run after clean up.
                            This is an OPTIONAL key.

                        no_of_streams   (int)       -- Number of streams to be used for restore

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                advanced_options    (dict)  -- Advanced restore options

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

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
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        if not isinstance(client, (str, Client)):
            raise SDKException('Subclient', '101')

        if isinstance(client, str):
            client = Client(self._commcell_object, client)

        if fs_options is not None and fs_options.get('no_of_streams', 1) > 1 and not fs_options.get('destination_appTypeId', False):
            fs_options['destination_appTypeId'] = int(client.agents.all_agents.get('file system', client.agents.all_agents.get('windows file system', client.agents.all_agents.get('linux file system', client.agents.all_agents.get('big data apps', client.agents.all_agents.get('cloud apps', 0))))))
            if not fs_options['destination_appTypeId']:
                del fs_options['destination_appTypeId']

            # check to find whether file level Restore/ Volume level restore for blocklevel.

        if fs_options is not None and fs_options.get('is_vlr_restore', False):
            if not (isinstance(paths, list) and
                    isinstance(overwrite, bool) and
                    isinstance(restore_data_and_acl, bool)):
                raise SDKException('Subclient', '101')

            paths = self._filter_paths(paths)

            if paths == []:
                raise SDKException('Subclient', '104')

            request_json = self._restore_json(
                client=client,
                paths=paths,
                overwrite=overwrite,
                restore_data_and_acl=restore_data_and_acl,
                copy_precedence=copy_precedence,
                from_time=from_time,
                to_time=to_time,
                destPath=destination_path,
                restore_option=fs_options
            )

            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(
                self._vlr_restore_options_dict)
            destination_options = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].get('destination', {})
            destination_options['destPath'] = destination_options.get('destPath', [''])
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination']['destPath'][0] = \
                destination_path
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination']['inPlace'] = False

            return self._process_restore_response(request_json)

        else:
            return super(FileSystemSubclient, self).restore_out_of_place(
                client=client,
                destination_path=destination_path,
                paths=paths,
                overwrite=overwrite,
                restore_data_and_acl=restore_data_and_acl,
                copy_precedence=copy_precedence,
                from_time=from_time,
                to_time=to_time,
                fs_options=fs_options,
                schedule_pattern=schedule_pattern,
                advanced_options=advanced_options
            )

    def enable_content_indexing(self, policy_id):
        """Enables Content indexing and add the policy associations"""
        update_properties = self.properties
        update_properties['fsSubClientProp']['enableContentIndexing'] = True
        update_properties['fsSubClientProp']['contentIndexingPolicy'] = int(policy_id)
        self.update_properties(update_properties)

    def disable_content_indexing(self):
        """Disables Content indexing and disassociate the CI policy"""
        update_properties = self.properties
        update_properties['fsSubClientProp']['enableContentIndexing'] = False
        self.update_properties(update_properties)

    @property
    def catalog_acl(self):
        """Gets the catalog acl option

        Returns:
            true  - if catalog acl is enbaled on the subclient

            false - if catalog acl disabled on the subclient
        """

        return self._fsSubClientProp['catalogACL']

    @catalog_acl.setter
    def catalog_acl(self, value):
        """
        To enable or disable catalog_acl
        Args:

            value   (bool)  -- To enable or disbale catalog acl
        """
        update_properties = self.properties
        if isinstance(value, bool):
            update_properties['fsSubClientProp']['catalogACL'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def index_server(self):
        """Returns the index server client set for the subclient. None if no Index Server is set"""

        if 'indexSettings' not in self._commonProperties:
            return None

        index_settings = self._commonProperties['indexSettings']
        index_server = None

        if ('currentIndexServer' in index_settings and
                'clientName' in index_settings['currentIndexServer']):
            index_server = index_settings['currentIndexServer']['clientName']

        if index_server is None:
            return None

        return Client(self._commcell_object, client_name=index_server)

    @index_server.setter
    def index_server(self, value):
        """Sets the index server client for the backupset

            Args:
                value   (object)    --  The index server client object to set

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        if not isinstance(value, Client):
            raise SDKException('Subclient', '121')

        index_server_name = value.client_name

        self._set_subclient_properties(
            "_commonProperties['indexSettings']['currentIndexServer']['clientName']",
            index_server_name)

    @property
    def index_pruning_type(self):
        """Treats the subclient pruning type as a read-only attribute."""

        index_settings = self._commonProperties['indexSettings']
        if 'indexPruningType' in index_settings:
            pruning_type = index_settings['indexPruningType']
            return pruning_type

    @property
    def index_pruning_days_retention(self):
        """Returns number of days to be maintained in index by index pruning for the subclient"""

        return self._commonProperties["indexSettings"]["indexRetDays"]

    @property
    def index_pruning_cycles_retention(self):
        """Returns number of cycles to be maintained in index by index pruning for the subclient"""

        return self._commonProperties["indexSettings"]["indexRetCycle"]

    @index_pruning_type.setter
    def index_pruning_type(self, value):
        """Updates the pruning type for the subclient when subclient level indexing is enabled.
        Can be days based pruning or cycles based pruning.
        Days based pruning will set index retention on the basis of days,
        cycles based pruning will set index retention on basis of cycles.

        Args:
            value    (str)  --  "days_based" or "cycles_based"

        """

        if value.lower() == "cycles_based":
            final_value = 1

        elif value.lower() == "days_based":
            final_value = 2

        elif value.lower() == "infinite":
            final_value = 0

        else:
            raise SDKException('Subclient', '119')

        self._set_subclient_properties(
            "_commonProperties['indexSettings']['indexPruningType']", final_value)

    @index_pruning_days_retention.setter
    def index_pruning_days_retention(self, value):
        """Sets index pruning days value at subclient level for days-based index pruning"""

        if isinstance(value, int) and value >= 2:
            self._set_subclient_properties(
                "_commonProperties['indexSettings']['indexRetDays']", value)
        else:
            raise SDKException('Subclient', '120')

    @index_pruning_cycles_retention.setter
    def index_pruning_cycles_retention(self, value):
        """Sets index pruning cycles value at subclient level for cycles-based index pruning"""

        if isinstance(value, int) and value > 0:
            self._set_subclient_properties(
                "_commonProperties['indexSettings']['indexRetCycle']", value)
        else:
            raise SDKException('Subclient', '120')

    @property
    def ibmi_dr_config(self):
        """
        Return the ibmi dr configuration

        Returns:
            (dict)  --  Dictionary of DR parameters
        """
        return {
            'backupMaxTime': self._fsSubClientProp.get('ibmiSubclientprop', {}).get('backupMaxTime', 0),
            'printSysInfo': self._fsSubClientProp.get('ibmiSubclientprop', {}).get('printSysInfo', False),
            'userProgram': self._fsSubClientProp.get('ibmiSubclientprop', {}).get('userProgram', ''),
            'saveSecData': self._fsSubClientProp.get('ibmiSubclientprop', {}).get('saveSecData', False),
            'saveConfObject': self._fsSubClientProp.get('ibmiSubclientprop', {}).get('saveConfObject', False)
        }

    @ibmi_dr_config.setter
    def ibmi_dr_config(self, dr_config):
        """
            Sets the subclient into one touch mode and adds ibmi DR parameters

            Args:
                dr_config   (dict)  --  Dictionary of IBMi DR parameters
                
                Example:
                    ibmi_dr_config = {
                        'backupMaxTime' : 120,
                        'printSysInfo' : True,
                        'userProgram' : 'QSYS/CVPGM',
                        'saveSecData' : True,
                        'saveConfObject' : False,
                        'library' : [{path:'/QSYS.LIB/TEST1.LIB'}]
                    }
            Returns:
                None

            Raises:
                SDKException:
                    if parameters are not valid
        """
        self.onetouch_option = True
        update_properties = self.properties
        if isinstance(dr_config, dict):
            update_properties['fsSubClientProp']['ibmiSubclientprop']= dr_config
        else:
            raise SDKException('Subclient', '102', 'The parameter should be a dictionary.')
        self.update_properties(update_properties)

    @property
    def backup_savf_file_data(self):
        """
         Return the ibmi savf file data configuration

        Returns:
            (bool)  --  Is savf file data going to be backed up
        """
        return self._fsSubClientProp.get('backupSaveFileData', False)

    @backup_savf_file_data.setter
    def backup_savf_file_data(self, value):
        """
        Sets the backup save file data property on an ibmi subclient
        Args:
                value   (boolean)  --  Toggle the backup property

            Returns:
                None

            Raises:
                None
        """
        update_properties = self.properties
        if isinstance(value, bool):
            update_properties['fsSubClientProp']['backupSaveFileData'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def backup_spool_file_data(self):
        """Gets the value of spool file data on ibmi option for IBMi subclient.

            Returns:
                False   -   if spool file data on IBMi is disabled on the subclient

                True    -   if spool file data on IBMi is enabled on the subclient
        """
        return bool(self._fsSubClientProp.get('backupSpooledFileData'))

    @backup_spool_file_data.setter
    def backup_spool_file_data(self, value):
        """Updates the generate signature property value on ibmi subclient.

            Args:
                value   (bool)  --  To enable or disable spool file data backup.
        """
        update_properties = self.properties
        if isinstance(value, bool):
            update_properties['fsSubClientProp']['backupSpooledFileData'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def backup_queue_data(self):
        """Gets the value of queue data data on ibmi option for IBMi subclient.

            Returns:
                False   -   if queue data on IBMi is disabled on the subclient

                True    -   if queue data on IBMi is enabled on the subclient
        """
        return bool(self._fsSubClientProp.get('backupQueueData'))

    @backup_queue_data.setter
    def backup_queue_data(self, value):
        """Updates the queue data property value on ibmi subclient.

            Args:
                value   (bool)  --  To enable or disable queue data backup.
        """
        update_properties = self.properties
        if isinstance(value, bool):
            update_properties['fsSubClientProp']['backupQueueData'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def backup_private_authorities(self):
        """Gets the value of private authorities on ibmi option for IBMi subclient.

            Returns:
                False   -   if PVTAUT on IBMi is disabled on the subclient

                True    -   if PVTAUT on IBMi is enabled on the subclient
        """
        return bool(self._fsSubClientProp.get('backupPrivateAuthority'))

    @backup_private_authorities.setter
    def backup_private_authorities(self, value):
        """Updates the private authorities property value on ibmi subclient.

            Args:
                value   (bool)  --  To enable or disable private authorities backup.
        """
        update_properties = self.properties
        if isinstance(value, bool):
            update_properties['fsSubClientProp']['backupPrivateAuthority'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def target_release(self):
        """Gets the value of target and release on ibmi option for IBMi subclient.

            Returns:
                (str)   -   Return the target and release string value
        """
        return bool(self._fsSubClientProp.get('targetReleaseForBackupData'))

    @target_release.setter
    def target_release(self, value):
        """Updates the private authorities property value on ibmi subclient.

            Args:
                value   (str)  --  To set target and release for  backup data.
        """
        update_properties = self.properties
        if isinstance(value, str):
            update_properties['fsSubClientProp']['targetReleaseForBackupData'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def save_access_path(self):
        """Gets the value of save access path on ibmi option for IBMi subclient.

            Returns:
                (str)   -   Return the save access path string value
        """
        return bool(self._fsSubClientProp.get('saveAccessPath'))

    @save_access_path.setter
    def save_access_path(self, value):
        """Updates the save access path property value on ibmi subclient.

            Args:
                value   (str)  --  To set access path value for  backup data.
        """
        update_properties = self.properties
        if isinstance(value, str):
            update_properties['fsSubClientProp']['saveAccessPath'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def update_history(self):
        """Gets the value of update history property on ibmi option for IBMi subclient.

            Returns:
                (str)   -   Return the string value of update history property
        """
        return bool(self._fsSubClientProp.get('updateHistory'))

    @update_history.setter
    def update_history(self, value):
        """Updates the update history property value on ibmi subclient.

            Args:
                value   (str)  --  To set update history value for  backup data.
        """
        update_properties = self.properties
        if isinstance(value, str):
            update_properties['fsSubClientProp']['updateHistory'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def ibmi_compression(self):
        """Gets the value of IBMi compression property on ibmi option for IBMi subclient.

            Returns:
                (str)   -   Return the string value of IBMi compression property
        """
        return bool(self._fsSubClientProp.get('ibmiCompression'))

    @ibmi_compression.setter
    def ibmi_compression(self, value):
        """Updates the IBMi compression property value on ibmi subclient.

            Args:
                value   (str)  --  To set IBMi compression value for  backup data.
        """
        update_properties = self.properties
        if isinstance(value, str):
            update_properties['fsSubClientProp']['ibmiCompression'] = value
        else:
            raise SDKException('Subclient', '101')
        self.update_properties(update_properties)

    @property
    def save_while_active_option(self):
        """
        Return the save while active options for an IBMi subclient.

        Returns:
             (dict) --  Dictionary of save while active options
        """
        return {
            'saveWhileActiveOpt': self._fsSubClientProp['saveWhileActiveOpt'],
            'activeWaitTime': self._fsSubClientProp['activeWaitTime']
        }

    @save_while_active_option.setter
    def save_while_active_option(self, swa_config):
        """
        Updates the save while active backup property for an IBMi subclient.

            Args:
                swa_config      (dict)  -- Dictionary of synclib config options

                    options                 --

                        saveWhileActiveOpt      (str)   --  Value of save while active option.

                        activeWaitTime          (int)   --  Amount of time to wait for check point.

        Returns:
            None

        Raises:
            SDKException:
                if failed to update the property of the subclient

                if value is invalid
        """
        update_properties = self.properties
        if isinstance(swa_config, dict):
            update_properties['fsSubClientProp'] = swa_config
        else:
            raise SDKException('Subclient', '102', 'SWA should be a dictionary.')
        self.update_properties(update_properties)

    @property
    def pre_post_commands(self):
        """
         Return the prep_post commands set for a subclient

        Returns:
            (dict)  --  All the pre/post commands
        """
        pre_scan_command = self._commonProperties["prepostProcess"]["preScanCommand"]
        post_scan_command = self._commonProperties["prepostProcess"]["postScanCommand"]
        pre_backup_command = self._commonProperties["prepostProcess"]["preBackupCommand"]
        post_backup_command = self._commonProperties["prepostProcess"]["postBackupCommand"]

        pre_post_commands = {'pre_scan_command': pre_scan_command, 'post_scan_command': post_scan_command, 'pre_backup_command': pre_backup_command, 'post_backup_command': post_backup_command}

        return pre_post_commands

    @pre_post_commands.setter
    def pre_post_commands(self, value):
        """
        Sets the pre post commands on a subclient
        Args:

            value   (dict)      --  Specifies the pre.post commands to be set

                pre_scan_command    (str)       --     The pre scan command to be set

                post_scan_command   (str)       --     The post scan command to be set

                pre_backup_command  (str)       --     The pre backup command to be set

                post_backup_command (str)       --     The post backup command to be set

            Returns:
                None

            Raises:
                None
        """
        if isinstance(value, dict):

            pre_post_process = self._commonProperties["prepostProcess"]

            pre_post_process["preScanCommand"] = value.get("pre_scan_command", "")
            pre_post_process["postScanCommand"] = value.get("post_scan_command", "")
            pre_post_process["preBackupCommand"] = value.get("pre_backup_command", "")
            pre_post_process["postBackupCommand"] = value.get("post_backup_command", "")

            self._set_subclient_properties('_commonProperties["prepostProcess"]', pre_post_process)

        else:
            raise SDKException('Subclient', '101')

    @property
    def backup_nodes(self):
        """
        Gets the backup nodes for FS Agent under Network Share Clients.
        """
        return self._fsSubClientProp["backupConfiguration"]["backupDataAccessNodes"]

    @backup_nodes.setter
    def backup_nodes(self, value):
        """
        Sets the backup nodes for FS Agent under Network Share Clients.

            Args:
                value  (list)   --  Specifies the nodes, a list of strings, values are data access node host names.
        """

        update_properties = self.properties

        access_nodes = []
        for access_node in value:
            access_nodes.append({"clientName": access_node})

        update_properties["fsSubClientProp"]["backupConfiguration"] = {"backupDataAccessNodes": access_nodes}
        self.update_properties(update_properties)

    @property
    def network_share_auto_mount(self):
        """
        Returns the value of enableNetworkShareAutoMount, if true, the content will be auto-mounted during backup and
        auto-mounted during in-place restores.
        """
        return self._fsSubClientProp['enableNetworkShareAutoMount']

    @network_share_auto_mount.setter
    def network_share_auto_mount(self, value):
        """
        Sets the value for enableNetworkShareAutoMount, needs to set to true if content is specified
        in the file_server:/path format.

            Args:
                value   (bool)  --  Enables or disables the property by setting True or False respectively.

        """
        update_properties = self.properties

        if isinstance(value, bool):
            update_properties["fsSubClientProp"]['enableNetworkShareAutoMount'] = value
        else:
            raise SDKException('Subclient', '101')

        self.update_properties(update_properties)

    @property
    def impersonate_user(self):
        """
        Returns the username ONLY and applicable to Windows FS subclients only.
        """
        return self._subclient_properties['impersonateUser']

    @impersonate_user.setter
    def impersonate_user(self, value):
        """
        Sets the user impersonation information for a subclient, applicable to Windows only.

        Args:

            value   (dict)  --  Valid keys are 'username' and 'password'

                username    (str)   --  The username

                password    (str)   --  The password
        """

        update_properties = self.properties

        if isinstance(value, dict):
            update_properties["impersonateUser"]["userName"] = value["username"]
            update_properties["impersonateUser"]["password"] = b64encode(value["password"].encode()).decode()

        self.update_properties(update_properties)

    @property
    def plan(self):
        """Returns the name of the plan associated with the subclient.
           Returns None if no plan is associated
        """
        return super().plan

    @plan.setter
    def plan(self, value):
        """Associates a plan to the subclient.

            Args:
                value   (object)    --  the Plan object which is to be associated
                                        with the subclient

                value   (str)       --  name of the plan to be associated
                
                value   (list)      --  associate subclient with Plan and override the content of Plan on subclient
                                        Example-1 ( with Plan name ): subclient_object.plan = ["plan_name",["content_path1","content_path2"]]
                                        Example-2 ( with Plan Object ): subclient_object.plan = [plan_object,["content_path1","content_path2"]]

                value   (None)      --  set value to None to remove plan associations
                

            Raises:
                SDKException:
                    if the type of input is incorrect

                    if the plan association is unsuccessful
        """
        
        from ..plan import Plan
        if isinstance(value, Plan):
            if self._commcell_object.plans.has_plan(value.plan_name):
                self.update_properties({
                    'planEntity': {
                        'planName': value.plan_name
                    },
                    "useContentFromPlan": True
                })
            else:
                raise SDKException('Subclient', '102', 'Plan does not exist')
                
        elif isinstance(value, str):
            if self._commcell_object.plans.has_plan(value):
                self.update_properties({
                    'planEntity': {
                        'planName': value
                    },
                    "useContentFromPlan": True
                })
            else:
                raise SDKException('Subclient', '102', 'Plan does not exist')
                
        elif isinstance(value, list):
            if not isinstance(value[0], Plan) and not isinstance(value[0], str):
                raise SDKException('Subclient', '102', 'Expecting Plan object or str')
            if not isinstance(value[1], list):
                raise SDKException('Subclient', '102', 'Expecting List of contents')
           
            self.update_properties({
                     "content": [{"path":p} for p in value[1]],
                    "useContentFromPlan": False,
                    "fsContentOperationType": 1,
                    'planEntity': {
                        'planName': value[0].plan_name if isinstance(value[0], Plan) else value[0]
                    }
                })
                
        elif value is None:
            self.update_properties({
                'removePlanAssociation': True
            })
        else:
            raise SDKException('Subclient', '101')
