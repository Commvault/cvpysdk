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

"""Main file for scheduler options related operations on the commcell.

This file has all the classes related to Schedule Options operations.

ScheduleOptions: Class for getting Schedule Options for Schedule and Schedule Policies

BackupOptions: Class for Backup Options for Schedule and Schedule Policies

AuxCopyOptions: Class for AuxCopy Options for Schedule and Schedule Policies

ScheduleOptions:

    __new__()       -- Returns the respective class object based on the option_type

    __init__()      --  initialises ScheduleOptions for Schedule and Schedule Policies

    options_json()  --  Returns the options json for the new options provided

BackupOptions:

    __init__()      --  initialises BackupOptions for Schedule and Schedule Policies

    options_json()  --  Returns the options json for the new backup options provided

AuxCopyOptions:

    __init__()      --  initialises AuxCopyOptions for Schedule and Schedule Policies

    options_json()  --  Returns the options json for the new AuxCopy options provided

"""

from abc import ABCMeta, abstractmethod

class ScheduleOptions:
    """Class for getting Schedule Options for Schedule and Schedule Policies."""

    __metaclass__ = ABCMeta

    #This map has to be updated with the subdict option_name for every new option class added
    policy_to_options_map = {

        'Data Protection': 'backupOpts',
        'Auxiliary Copy': 'auxcopyJobOption'
    }

    def __new__(cls, options_type, current_options=None):
        """
        Returns the respective class object based on the option_type

        Args:
            options_type (str) -- option type as per ScheduleOptions.options dict.
            current_options (dict) -- current options set for the schedule if any.

        Returns (obj) -- Return the class object based on the option_type

        """

        #This dict has to be update with the option_name and corresponding Option class created
        options = {

            'backupOpts': BackupOptions,
            'auxcopyJobOption': AuxCopyOptions

        }
        #subclass inherit __new__ method so we need this if check to initialize parent.
        if cls is not __class__:
            return super().__new__(cls)
        return options[options_type](current_options)




    def __init__(self, options_type, current_options=None):
        """
        Initialises Schedule Options class
        Args:
            options_type (str) -- option type as per ScheduleOptions.options dict.
            current_options (dict) -- current options set for the schedule if any.
        """
        if current_options:
            self.current_options = current_options
        else:
            self.current_options = {}

    @abstractmethod
    def options_json(self, new_options=None):
        """
        Returns the options json for the new options provided
        Args:
            new_options: options_json based on the type of scheduler option

        Returns (dict) -- new options

        """


class BackupOptions(ScheduleOptions):
    """Class for getting Backup Schedule Options for Schedule and Schedule Policies."""
    def __init__(self, options_type, current_options=None):
        """
        Initialises the BackupOptions class
        Args:
            options_type (str) -- should be 'backupOpts'
            current_options (dict) -- current backup options set for the schedule if any.
        """
        super().__init__(options_type, current_options)

    def options_json(self, new_options=None):
        """

        Returns the backup options json for the new options provided

        Args:
             new_options (dict) -- options which need to be set for the schedule
                                    Example:
                                     {
                                        "backupLevel": backup_level(Full / Incremental / Differential / Synthetic_full),
                                        "incLevel": incremental_level(BEFORE_SYNTH / AFTER_SYNTH),
                                        "runIncrementalBackup": incremental_backup
                                    }
        Returns (dict) -- new options


        """
        if not new_options:
            new_options = {}
        if self.current_options:
            for key, value in new_options.items():
                self.current_options[key] = value
            return {'backupOpts': self.current_options}

        default_dict = {
            "backupLevel": "Incremental",
            "incLevel": 1,
            "runIncrementalBackup": False
        }

        new_options = dict(default_dict, **new_options)
        return {'backupOpts': new_options}


class AuxCopyOptions(ScheduleOptions):
    """Class for getting AuxCopy Schedule Options for Schedule and Schedule Policies."""
    def __init__(self, options_type, current_options=None):
        """
        Initialises the AuxCopyOptions class
        Args:
            options_type (str) -- should be 'auxcopyJobOption'
            current_options (dict) -- current AuxCopy options set for the schedule if any.
        """
        super().__init__(options_type, current_options)

    def options_json(self, new_options=None):
        """

        Returns the AuxCopy options json for the new options provided

        Args:
             new_options (dict) -- options which need to be set for the schedule
                                    Example:
                                    {
                                        "maxNumberOfStreams": 0,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": True,
                                        "totalJobsToProcess": 1000,
                                        "allCopies": True,
                                        "mediaAgent": {
                                            "mediaAgentName": "<ANY MEDIAAGENT>"
                                        }
                                    }
        """
        if not new_options:
            new_options = {}
        if self.current_options:
            for key, value in new_options.items():
                self.current_options[key] = value
            return {'backupOpts':
                        {
                            'mediaOpt':
                                {
                                    'auxcopyJobOption': self.current_options
                                }
                        }
                    }

        default_dict = {
            "maxNumberOfStreams": 0,
            "useMaximumStreams": True,
            "useScallableResourceManagement": True,
            "totalJobsToProcess": 1000,
            "allCopies": True,
            "mediaAgent": {
                "mediaAgentName": "<ANY MEDIAAGENT>"
            }
        }

        new_options = dict(default_dict, **new_options)

        return {
            'backupOpts':
            {
                'mediaOpt':
                    {
                        'auxcopyJobOption': new_options
                    }
            }
            }
