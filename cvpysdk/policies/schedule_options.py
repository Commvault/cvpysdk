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
from typing import Optional, Dict, Any


class ScheduleOptions:
    """Class for getting Schedule Options for Schedule and Schedule Policies.

    Attributes:
        policy_to_options_map (dict): A mapping of policy types to option names.

    Usage:
        # Example of accessing the policy_to_options_map attribute
        options_map = ScheduleOptions.policy_to_options_map
    """

    __metaclass__ = ABCMeta

    # This map has to be updated with the subdict option_name for every new option class added
    policy_to_options_map = {
        'Data Protection': 'backupOpts',
        'Auxiliary Copy': 'auxcopyJobOption'
    }

    def __new__(cls, options_type: str, current_options: Optional[Dict[str, Any]] = None) -> 'ScheduleOptions':
        """Returns the respective class object based on the option_type.

        Args:
            options_type (str): option type as per ScheduleOptions.options dict.
            current_options (dict, optional): current options set for the schedule if any. Defaults to None.

        Returns:
            ScheduleOptions: Return the class object based on the option_type

        Usage:
            # Example of creating a BackupOptions object
            backup_options = ScheduleOptions('backupOpts')

            # Example of creating an AuxCopyOptions object with current options
            current_options = {'maxNumberOfStreams': 10}
            aux_copy_options = ScheduleOptions('auxcopyJobOption', current_options)
        """
        # This dict has to be update with the option_name and corresponding Option class created
        options = {
            'backupOpts': BackupOptions,
            'auxcopyJobOption': AuxCopyOptions
        }
        # subclass inherit __new__ method so we need this if check to initialize parent.
        if cls is not ScheduleOptions:
            return super().__new__(cls)
        return options[options_type](options_type, current_options)

    def __init__(self, options_type: str, current_options: Optional[Dict[str, Any]] = None) -> None:
        """Initialises Schedule Options class.

        Args:
            options_type (str): option type as per ScheduleOptions.options dict.
            current_options (dict, optional): current options set for the schedule if any. Defaults to None.

        Usage:
            # Example of initializing ScheduleOptions with current options
            current_options = {'backupLevel': 'Full'}
            schedule_options = ScheduleOptions('backupOpts', current_options)
        """
        if current_options:
            self.current_options = current_options
        else:
            self.current_options = {}

    @abstractmethod
    def options_json(self, new_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Returns the options json for the new options provided.

        Args:
            new_options (dict, optional): options_json based on the type of scheduler option. Defaults to None.

        Returns:
            dict: new options

        Usage:
            # This is an abstract method and needs to be implemented in subclasses.
            pass
        """
        pass


class BackupOptions(ScheduleOptions):
    """Class for getting Backup Schedule Options for Schedule and Schedule Policies.

    Usage:
        # Example of creating a BackupOptions object
        backup_options = BackupOptions('backupOpts')
    """

    def __init__(self, options_type: str, current_options: Optional[Dict[str, Any]] = None) -> None:
        """Initialises the BackupOptions class.

        Args:
            options_type (str): should be 'backupOpts'
            current_options (dict, optional): current backup options set for the schedule if any. Defaults to None.

        Usage:
            # Example of initializing BackupOptions with current options
            current_options = {'backupLevel': 'Full'}
            backup_options = BackupOptions('backupOpts', current_options)
        """
        super().__init__(options_type, current_options)

    def options_json(self, new_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Returns the backup options json for the new options provided.

        Args:
             new_options (dict, optional): options which need to be set for the schedule. Defaults to None.

        Returns:
            dict: new options

        Usage:
            # Example of setting new backup options
            new_options = {
                "backupLevel": "Full",
                "incLevel": 0,
                "runIncrementalBackup": True
            }
            backup_options = BackupOptions('backupOpts')
            options_json = backup_options.options_json(new_options)

            # Example of setting new backup options with current options
            current_options = {"backupLevel": "Incremental", "incLevel": 1, "runIncrementalBackup": False}
            new_options = {"backupLevel": "Full"}
            backup_options = BackupOptions('backupOpts', current_options)
            options_json = backup_options.options_json(new_options)
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
    """Class for getting AuxCopy Schedule Options for Schedule and Schedule Policies.

    Usage:
        # Example of creating an AuxCopyOptions object
        aux_copy_options = AuxCopyOptions('auxcopyJobOption')
    """

    def __init__(self, options_type: str, current_options: Optional[Dict[str, Any]] = None) -> None:
        """Initialises the AuxCopyOptions class.

        Args:
            options_type (str): should be 'auxcopyJobOption'
            current_options (dict, optional): current AuxCopy options set for the schedule if any. Defaults to None.

        Usage:
            # Example of initializing AuxCopyOptions with current options
            current_options = {'maxNumberOfStreams': 10}
            aux_copy_options = AuxCopyOptions('auxcopyJobOption', current_options)
        """
        super().__init__(options_type, current_options)

    def options_json(self, new_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Returns the AuxCopy options json for the new options provided.

        Args:
             new_options (dict, optional): options which need to be set for the schedule. Defaults to None.

        Returns:
            dict: The aux copy options json.

        Usage:
            # Example of setting new aux copy options
            new_options = {
                "maxNumberOfStreams": 10,
                "useMaximumStreams": False,
                "useScallableResourceManagement": False,
                "totalJobsToProcess": 500,
                "allCopies": False,
                "mediaAgent": {
                    "mediaAgentName": "MediaAgent001"
                }
            }
            aux_copy_options = AuxCopyOptions('auxcopyJobOption')
            options_json = aux_copy_options.options_json(new_options)

            # Example of setting new aux copy options with current options
            current_options = {
                "maxNumberOfStreams": 0,
                "useMaximumStreams": True,
                "useScallableResourceManagement": True,
                "totalJobsToProcess": 1000,
                "allCopies": True,
                "mediaAgent": {
                    "mediaAgentName": "<ANY MEDIAAGENT>"
                }
            }
            new_options = {"maxNumberOfStreams": 10}
            aux_copy_options = AuxCopyOptions('auxcopyJobOption', current_options)
            options_json = aux_copy_options.options_json(new_options)
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
