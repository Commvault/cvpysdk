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

"""Main file for performing storage policy related operations on the commcell.

This file has all the classes related to Storage Policy operations.

StoragePolicies:  Class for representing all the Storage Policies associated to the commcell.

StoragePolicy:    Class for representing a single Storage Policy associated to the commcell.


StoragePolicies:
    __init__(commcell_object)    --  initialize the StoragePolicies instance for the commcell

    __str__()                    --  returns all the storage policies associated with the commcell

    __repr__()                   --  returns a string for the instance of the StoragePolicies class

    _get_policies()              --  gets all the storage policies of the commcell

    all_storage_policies()       --  returns the dict of all the storage policies on commcell

    has_policy(policy_name)      --  checks if a storage policy exists with the given name

    add_global_storage_policy()  --  adds a new global storage policy to the commcell

    add()                        --  adds a new storage policy to the commcell

    add_tape_sp()                --  add new storage policy with tape library as data path

    delete(storage_policy_name)  --  removes the specified storage policy from the commcell

    refresh()                    --  refresh the storage policies associated with the commcell


StoragePolicy:
    __init__(commcell_object,
             storage_policy_name,
             storage_policy_id)             --  initialize the instance of StoragePolicy class for
    a specific storage policy of the commcell


    __repr__()                              --  returns a string representation of the
    StoragePolicy instance

    _get_storage_policy_id()                --  gets the id of the StoragePolicy instance

    _get_storage_policy_properties()        --  returns the properties of this storage policy

    _get_storage_policy_advanced_properties()--  returns the advanced properties of this storage policy

    _initialize_storage_policy_properties() --  initializes storage policy properties

    has_copy()                              --  checks if copy with given name exists

    create_secondary_copy()                 --  creates a storage policy copy

    create_snap_copy()                      --  creates snap, snapvault, snapmirror, replica
                                                and replica mirror copies

    create_dedupe_secondary_copy()          --  create secondary copy with dedupe enabled

    delete_secondary_copy()                 --  deletes storage policy copy

    copies()                                --  returns the storage policy copies associated with
    this storage policy

    get_copy_precedence()                   --  returns the copy precedence value associated with
    the copy name

    update_snapshot_options()               --  Method for Updating Backup Copy and Snapshot
    Catalog Options

    run_backup_copy()                       --  Runs the backup copy job from Commcell

    modify_dynamic_stream_allocation()      --  modifies dsa property of storage policy

    run_snapshot_cataloging()               --  Runs the deferred catalog job from Commcell

    run_aux_copy()                          --  starts a aux copy job for this storage policy and
    returns the job object

    refresh()                               --  refresh the properties of the storage policy

    update_transactional_ddb()              --  enable/disable transactional DDB option on a DDB

    seal_ddb()                              --  seal a DDB store

    add_ddb_partition()                     --  Adds a new DDB partition

    move_dedupe_store()                     --  Moves a deduplication store

    run_ddb_verification()                  --  Runs DDB verification job

    run_data_verification()                 --  Runs Data Verification Job

    get_copy()                              --  Returns the StoragePolicyCopy class object of the input copy

    get_primary_copy()                      --  Returns the primary copy of the storage policy

    get_secondary_copies()                  --  Returns all the secondary copies in the storage policy sorted
    by copy precedence

    mark_for_recovery()                     --  Marks Deduplication store for recovery

    run_recon()                             --  Runs non-mem DB Reconstruction job

    reassociate_all_subclients()            --  Reassociates all subclients associated to Storage Policy

    enable_entity_extraction()              --  Enables the entity extraction for subclients associated to this policy

    enable_content_indexing()               --  Enables the content indexing for this storage policy

    run_content_indexing()                  --  start the content indexing job for this storage policy

    start_over()                            --  performs start over operation on storage policy/gdsp

    run_data_forecast()                     -- runs granular data forecast operation for given storage policy


StoragePolicyCopy:
    __init__(self, commcell_object,
                storage_policy_name,
                copy_name, copy_id)         --  initialize the instance of StoragePolicy class for
                                                a specific storage policy of the commcell

    __repr__()                              --  returns a string representation of the
                                                StoragePolicy instance

    copy_name()                         --  Gets the name of the storage policy copy

    get_copy_id()		                    --	Gets the storage policy id asscoiated with the storage policy

    get_copy_Precedence()                   --  Gets the copy precendence associated with the storage policy copy

    refresh()		                        --	Refresh the properties of the StoragePolicy

    _get_request_json()	                    --	Gets all the storage policy copy properties

    _get_copy_properties()	                --	Gets the storage policy copy properties

    _set_copy_properties()	                --	sets the properties of this storage policy copy

    set_copy_software_compression()         --  Sets the copy software compression setting

    is_parallel_copy()                      --  Gets the parallel copy setting on storage policy copy

    set_parallel_copy()                     --  Sets the parallel copy setting on storage policy copy

    is_inline_copy()                        --  Gets the inline copy setting on storage policy copy

    set_inline_copy()                       --  Sets the inline copy setting on storage policy copy

    get_jobs_on_copy()                      --  Fetches the Details of jobs on Storage Policy Copy

    delete_job()                            --  delete a job from storage policy copy node

    _mark_jobs_on_copy()                    --  marks job(s) for given operation on a secondary copy

    pick_for_copy()                         --  marks job(s) to be Picked for Copy to a secondary copy

    recopy_jobs()                           --  marks job(s) to be picked for ReCopying to a secondary copy

    do_not_copy_jobs()                      --  marks job(s) as Do Not Copy to a secondary copy

    pick_jobs_for_data_verification()       --  marks job(s) on a copy to be Picked for Data Verification

    do_not_verify_data()                    --  marks job(s) on a copy to not be Picked for Data Verification

    mark_jobs_bad()                         --  marks job(s) on a copy as Bad

    is_dedupe_enabled()                     --  checks whether deduplication is enabled for the copy

    set_encryption_properties()                   --  configures copy encryption settings as per user input

    set_key_management_server()             --  sets the Key Management Server to this copy

    set_multiplexing_factor()               --  sets/unset the multiplexing factor for the storage policy copy 

Attributes
----------
    **override_pool_retention**                 --  Returns if Override Pool Retention flag is set or not

    **override_pool_retention.setter**          --  Sets/Unsets the override Pool Retention Flag

    **space_optimized_auxillary_copy**          --  Returns the value of space optimized auxillary copy setting

    **space_optimized_auxillary_copy.setter**   --  Sets the value of space optimized auxillary copy setting

    **source_copy**                             --  Returns the source copy associated with the copy

    **source_copy.setter**                      --  Sets the source copy for the copy

    **store_priming**                    --  Sets the value of DDB store priming under copy dedupe properties

    ***is_active***                             --  Returns/Sets the 'Active' Property of the Copy

    ***network_throttle_bandwidth***            --  Returns/Sets the value of Network Throttle Bandwidth
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode

from ..exception import SDKException
from ..job import Job
from ..schedules import Schedules, SchedulePattern

from ..storage import DiskLibrary
from ..storage import MediaAgent


class StoragePolicies(object):
    """Class for getting all the storage policies associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the StoragePolicies class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the StoragePolicies class
        """
        self._commcell_object = commcell_object
        self._POLICY = self._commcell_object._services['STORAGE_POLICY']
        self._DELETE_POLICY =  self._commcell_object._services['DELETE_STORAGE_POLICY']
        self._policies = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all storage policies of the commcell.

            Returns:
                str - string of all the storage policies associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Storage Policy')

        for index, policy in enumerate(self._policies):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, policy)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Clients class."""
        return "StoragePolicies class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_policies(self):
        """Gets all the storage policies associated to the commcell specified by commcell object.

            Returns:
                dict - consists of all storage policies of the commcell
                    {
                         "storage_policy1_name": storage_policy1_id,
                         "storage_policy2_name": storage_policy2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._POLICY + "?getAll=TRUE")

        if flag:
            if response.json() and 'policies' in response.json():
                policies = response.json()['policies']

                if policies == []:
                    return {}

                policies_dict = {}

                for policy in policies:
                    temp_name = policy['storagePolicyName'].lower()
                    temp_id = str(policy['storagePolicyId']).lower()
                    policies_dict[temp_name] = temp_id

                return policies_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_storage_policies(self):
        """Returns dict of all the storage policies on this commcell

            dict - consists of all storage policies of the commcell
                    {
                         "storage_policy1_name": storage_policy1_id,
                         "storage_policy2_name": storage_policy2_id
                    }
        """
        return self._policies

    def has_policy(self, policy_name):
        """Checks if a storage policy exists in the commcell with the input storage policy name.

            Args:
                policy_name (str)  --  name of the storage policy

            Returns:
                bool - boolean output whether the storage policy exists in the commcell or not

            Raises:
                SDKException:
                    if type of the storage policy name argument is not string
        """
        if not isinstance(policy_name, str):
            raise SDKException('Storage', '101')

        return self._policies and policy_name.lower() in self._policies

    def get(self, storage_policy_name):
        """Returns a StoragePolicy object of the specified storage policy name.

            Args:
                storage_policy_name     (str)   --  name of the storage policy

            Returns:
                object - instance of the StoragePolicy class for the given policy name

            Raises:
                SDKException:
                    if type of the storage policy name argument is not string

                    if no storage policy exists with the given name
        """
        if not isinstance(storage_policy_name, str):
            raise SDKException('Storage', '101')

        storage_policy_name = storage_policy_name.lower()

        if self.has_policy(storage_policy_name):
            return StoragePolicy(
                self._commcell_object, storage_policy_name, self._policies[storage_policy_name]
            )
        else:
            raise SDKException(
                'Storage', '102', 'No policy exists with name: {0}'.format(storage_policy_name)
            )

    def add_global_storage_policy(self,
                                  global_storage_policy_name,
                                  library,
                                  media_agent,
                                  dedup_path=None,
                                  dedup_path_media_agent=None):
        """adds a global storage policy

            Args:
                global_storage_policy_name   (str)  --  name of the global storage policy which you want to add

                library                      (str)  --  name of the library which you want to be associated with your
                global storage policy

                media_agent                  (str)  --  name of the media agent which you want to be associated with
                the global storage policy

                        *enter BOTH, the dedup_path and dedup_path_media_agent if you want the deduplication
                         to be enabled.

                dedup_path                    (str) -- path of the deduplication database
                default- None

                dedup_path_media_agent:       (str) -- name of the media agent where the deduplication database
                                                       is stored
                default- None

            Returns:
                    the success message along with the name of the global storage policy if created successfully
                    else the error messages or the exceptions raised

            Raises:
                SDKException:
                        if the global_storage_policy_name,library,media_agent,dedup_path,dedup_path_media_agent
                        is not of type String

                        if response is empty

                        if response is not success

        """

        if not (isinstance(global_storage_policy_name, str) and
                isinstance(library, str) and
                isinstance(media_agent, str)):
            raise SDKException("Storage", "101")

        if ((dedup_path is not None and not isinstance(dedup_path, str)) or
                dedup_path_media_agent is not None and not isinstance(dedup_path_media_agent, str)):
            raise SDKException("Storage", "101")

        request_json = {
            "storagePolicyName": global_storage_policy_name,
            "copyName": "Primary_Global",
            "storagePolicyCopyInfo": {
                "storagePolicyFlags": {
                    "globalStoragePolicy": 1
                },
                "library": {
                    "libraryName": library
                },
                "mediaAgent": {
                    "mediaAgentName": media_agent
                },
                "retentionRules": {
                    "retainArchiverDataForDays": -1,
                    "retainBackupDataForCycles": -1,
                    "retainBackupDataForDays": -1
                }
            }
        }

        if dedup_path is not None and dedup_path_media_agent is not None:
            storage_policy_copy_info = {
                "dedupeFlags": {
                    "enableDASHFull": 1,
                    "hostGlobalDedupStore": 1,
                    "enableDeduplication": 1
                },
                "storagePolicyFlags": {
                    "blockLevelDedup": 1,
                    "enableGlobalDeduplication": 1
                },
                "DDBPartitionInfo": {
                    "maInfoList": [
                        {
                            "mediaAgent": {
                                "mediaAgentName": dedup_path_media_agent
                            },
                            "subStoreList": [
                                {
                                    "diskFreeWarningThreshholdMB": 10240,
                                    "diskFreeThresholdMB": 5120,
                                    "accessPath": {
                                        "path": dedup_path
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
            request_json["storagePolicyCopyInfo"].update(storage_policy_copy_info)

        # don't create dedup global storage policy if the arguments are not supplied
        elif(dedup_path or dedup_path_media_agent):
            raise SDKException("Storage", "101", "cannot create dedup global policy without complete arguments \n"
                               "supply both dedup path and dedup path media agent")

        # checking to create non dedup global storage policy
        elif(dedup_path is None and dedup_path_media_agent is None):
            storage_policy_copyinfo = {
                "extendedFlags": {
                    "globalStoragePolicy": 1
                }
            }
            request_json["storagePolicyCopyInfo"].update(storage_policy_copyinfo)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._POLICY, request_json
        )

        if flag:
            if response.json():
                if 'error' in response.json() and response.json()['error']['errorCode'] == 0:
                    # initialize the policies again
                    # so the policies object has all the policies
                    self.refresh()

                else:
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create storage policy\nError: "{0}"'

                    raise SDKException('Storage', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return self.get(global_storage_policy_name)

    def add(self,
            storage_policy_name,
            library=None,
            media_agent=None,
            dedup_path=None,
            incremental_sp=None,
            retention_period=5,
            number_of_streams=None,
            ocum_server=None,
            dedup_media_agent=None,
            dr_sp=False,
            **kwargs):
        """Adds a new Storage Policy to the Commcell.

            Args:
                storage_policy_name (str)         --  name of the new storage policy to add

                library             (str/object)  --  name or instance of the library
                to add the policy to

                media_agent         (str/object)  --  name or instance of media agent
                to add the policy to

                dedup_path          (str)         --  the path of the deduplication database
                default: None

                incremental_sp      (str)         --  the name of the incremental storage policy
                associated with the storage policy
                default: None

                retention_period    (int)         --  time period in days to retain
                the data backup for
                default:5

                number_of_streams   (int)         --  the number of streams for the storage policy
                default: None

                ocum_server         (str)         --  On Command Unified Server Name
                default: None

                dedup_media_agent   (str)          --  name of media agent where deduplication database is hosted.
                default:None

                dr_sp                (bool)         --  if True creates dr storage policy
                                                        if False creates data protection policy
                default:False

                **kwargs    --  dict of keyword arguments as follows:

                    global_policy_name   (str)         --  name of the global storage policy on which you want
                                                           the policy being created to be dependent.

                    global_dedup_policy (bool)  -- whether the global storage policy has a global deduplication pool
                                                   or not
                    default:True                  (meaning the global storage policy will have deduplication enabled)

            Raises:
                SDKException:
                    if type of the storage policy name argument is not string

                    if type of the retention period argument is not int

                    if type of the library argument is not either string or DiskLibrary instance

                    if type of the media agent argument is not either string or MediaAgent instance

                    if failed to create storage policy

                    if response is empty

                    if response is not success
        """

        extra_arguments = {
            'global_policy_name': None,
            'global_dedup_policy': True
        }
        # if global_dedup_policy will always have some value
        # global_policy_name decides if user wants to create sp using existing global dedup policy or not
        extra_arguments.update(kwargs)

        if ((dedup_path is not None and not isinstance(dedup_path, str)) or
                (not (isinstance(storage_policy_name, str) and
                      isinstance(retention_period, int))) or
                (incremental_sp is not None and not isinstance(incremental_sp, str))):
            raise SDKException('Storage', '101')

        if isinstance(library, DiskLibrary):
            disk_library = library
        elif isinstance(library, str):
            disk_library = DiskLibrary(self._commcell_object, library)
        elif extra_arguments["global_policy_name"] is not None:
            pass
            # when existing global_dedup_policy is used then library details not needed
        else:
            raise SDKException('Storage', '104')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, str):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        elif extra_arguments["global_policy_name"] is not None:
            pass
            # when existing global_dedup_policy is used then MA details not needed
        else:
            raise SDKException('Storage', '103')

        sp_type = 2 if dr_sp else 1

        if extra_arguments["global_policy_name"] is None:
            # then populate request json using supplied Library, MA and dedup path
            request_json = {
                "storagePolicyCopyInfo": {
                    "library": {
                        "libraryId": int(disk_library.library_id)
                    },
                    "mediaAgent": {
                        "mediaAgentId": int(media_agent.media_agent_id)
                    },
                    "retentionRules": {
                        "retainBackupDataForDays": retention_period
                    }
                },
                "storagePolicyName": storage_policy_name,
                "type": sp_type
            }

            if dedup_path:
                if dedup_media_agent is None:
                    dedup_media_agent = media_agent
                elif self._commcell_object.media_agents.has_media_agent(dedup_media_agent):
                    dedup_media_agent = MediaAgent(self._commcell_object, dedup_media_agent)
                else:
                    raise SDKException('Storage', '103')

                dedup_info = {
                    "storagePolicyCopyInfo": {
                        "dedupeFlags": {
                            "enableDeduplication": 1
                        },
                        "DDBPartitionInfo": {
                            "maInfoList": [{
                                "mediaAgent": {
                                    "mediaAgentName": dedup_media_agent.media_agent_name
                                },
                                "subStoreList": [{
                                    "accessPath": {
                                        "path": dedup_path
                                    }
                                }]
                            }]
                        }
                    }
                }

                request_json["storagePolicyCopyInfo"].update(dedup_info["storagePolicyCopyInfo"])

        # since we are supplying a global policy thus there is no need of the
        # dedup store details and the library details which got included above,
        # it will take up the settings of the global storage policy
        # thus defining request_json

        if extra_arguments["global_policy_name"] is not None and extra_arguments["global_dedup_policy"] is True:
            request_json = {
                "storagePolicyCopyInfo": {
                    "useGlobalPolicy": {
                        "storagePolicyName": extra_arguments["global_policy_name"]
                    },
                    "retentionRules": {
                        "retainBackupDataForDays": retention_period
                    },
                    "dedupeFlags": {
                        "useGlobalDedupStore": 1,
                        "enableClientSideDedup": 1,
                        "enableDASHFull": 1,
                        "enableDeduplication": 1
                    }
                },
                "storagePolicyName": storage_policy_name
            }

        elif extra_arguments["global_policy_name"] is not None and extra_arguments["global_dedup_policy"] is False:
            request_json = {
                "storagePolicyName": storage_policy_name,
                "storagePolicyCopyInfo": {
                    "dedupeFlags": {
                        "enableDASHFull": 1
                    },
                    "retentionRules": {
                        "retainBackupDataForDays": retention_period
                    },
                    "extendedFlags": {
                        "useGlobalStoragePolicy": 1
                    },
                    "useGlobalPolicy": {
                        "storagePolicyName": extra_arguments["global_policy_name"]
                    }
                }
            }

        if number_of_streams is not None:
            number_of_streams_dict = {
                "numberOfStreams": number_of_streams
            }
            request_json.update(number_of_streams_dict)

        if ocum_server is not None:
            ocum_server_dict1 = {
                "dfmServer": {
                    "name": ocum_server,
                    "id": 0
                }
            }
            ocum_server_dict2 = {
                "storagePolicyCopyInfo": {
                    "snapLibrary": {
                        "libraryName": "Use primary copy's library and mediaAgent"
                    },
                    "storagePolicyFlags": {
                        "enableSnapshot": 1
                    }
                }
            }

            request_json["storagePolicyCopyInfo"].update(ocum_server_dict2["storagePolicyCopyInfo"])
            request_json.update(ocum_server_dict1)

        if incremental_sp:
            incremental_sp_info = {
                "incrementalStoragePolicy": {
                    "storagePolicyName": incremental_sp
                }
            }

            request_json.update(incremental_sp_info)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._POLICY, request_json
        )

        if flag:
            if response.json():
                if 'error' in response.json() and response.json()['error']['errorCode'] == 0:
                    # initialize the policies again
                    # so the policies object has all the policies
                    self.refresh()

                else:
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create storage policy\nError: "{0}"'

                    raise SDKException('Storage', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return self.get(storage_policy_name)

    def add_tape_sp(self, storage_policy_name, library, media_agent, drive_pool, scratch_pool, retention_period_days=15,
                    ocum_server=None):
        """
        Adds storage policy with tape data path
        Args:
                storage_policy_name (str)         --  name of the new storage policy to add

                library             (str)     --  name or instance of the library
                to add the policy to

                media_agent         (str/object)  --  name or instance of media agent
                to add the policy to

                drive_pool          (str)         --  Drive pool name of the tape library

                scratch_pool      (str)          --  Scratch pool name of the tape library

                retention_period_days    (int)         --  time period in days to retain
                the data backup for
                default: 15

                ocum_server         (str)         --  On Command Unified Server Name
                default: None

            Raises:
                SDKException:
                    if type of the storage policy name argument is not string

                    if type of the retention period argument is not int

                    if type of the library argument is not either string or DiskLibrary instance

                    if type of the media agent argument is not either string or MediaAgent instance

                    if failed to create storage policy

                    if response is empty

                    if response is not success
        """
        tape_library = library
        if not (isinstance(drive_pool, str) and
                isinstance(scratch_pool, str) and
                isinstance(tape_library, str) and
                isinstance(media_agent, str) and
                isinstance(storage_policy_name, str) and
                (retention_period_days is None or isinstance(retention_period_days, int))):
            raise SDKException('Storage', '101')

        request_json = {
            "storagePolicyCopyInfo": {
                "retentionRules": {
                    "retainBackupDataForDays": retention_period_days
                },
                "library": {
                    "libraryName": tape_library
                },
                "mediaAgent": {
                    "mediaAgentName": media_agent
                }
            },
            "drivePool": drive_pool,
            "scratchpool": scratch_pool,
            "storagePolicyName": storage_policy_name
        }

        if ocum_server is not None:
            ocum_server_dict1 = {
                "dfmServer": {
                    "name": ocum_server,
                    "id": 0
                }
            }

            ocum_server_dict2 = {
                "storagePolicyCopyInfo": {
                    "snapLibrary": {
                        "libraryName": "Use primary copy's library and mediaAgent"
                    },
                    "storagePolicyFlags": {
                        "enableSnapshot": 1
                    }
                }
            }

            request_json["storagePolicyCopyInfo"].update(ocum_server_dict2["storagePolicyCopyInfo"])
            request_json.update(ocum_server_dict1)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._POLICY, request_json
        )

        if flag:
            if response.json():
                if 'error' in response.json() and response.json()['error']['errorCode'] == 0:
                    # initialize the policies again
                    # so the policies object has all the policies
                    self.refresh()

                else:
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create storage policy with tape data path\nError: "{0}"'

                    raise SDKException('Storage', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return self.get(storage_policy_name)

    def delete(self, storage_policy_name):
        """Deletes a storage policy from the commcell.

            Args:
                storage_policy_name (str)  --  name of the storage policy to delete

            Raises:
                SDKException:
                    if type of the storage policy name argument is not string

                    if failed to delete storage policy

                    if response is empty

                    if response is not success
        """
        if not isinstance(storage_policy_name, str):
            raise SDKException('Storage', '101')

        if self.has_policy(storage_policy_name):
            storagepolicy_id = self.all_storage_policies[storage_policy_name.lower()]
            policy_delete_service = self._DELETE_POLICY + '/{0}'.format(storagepolicy_id)

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', policy_delete_service
            )

            if flag:
                try:
                    if response.json():
                        if 'error' in response.json():
                            if 'errorCode' in response.json()['error'] and 'errorMessage' in response.json()['error']:
                                error_message = response.json()['error']['errorMessage']
                                o_str = 'Failed to delete storage policy\nError: "{0}"'

                                raise SDKException('Storage', '102', o_str.format(error_message))
                            elif 'errorCode' in response.json()['error'] and response.json()['error']['errorCode'] == 0:
                                self.refresh()
                                return response.text.strip()
                except ValueError:
                    if response.text:
                        if 'errorCode' in response.text and 'errorMessage' in response.text:
                            raise SDKException('Storage', '102', response.text.strip())
                        self.refresh()
                        return response.text.strip()
                    else:
                        raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Storage', '102', 'No policy exists with name: {0}'.format(storage_policy_name)
            )

    def refresh(self):
        """Refresh the storage policies associated with the Commcell."""
        self._policies = self._get_policies()


class StoragePolicy(object):
    """Class for performing storage policy operations for a specific storage policy"""

    def __init__(self, commcell_object, storage_policy_name, storage_policy_id=None):
        """Initialise the Storage Policy class instance."""
        self._storage_policy_name = storage_policy_name.lower()
        self._commcell_object = commcell_object

        if storage_policy_id:
            self._storage_policy_id = str(storage_policy_id)
        else:
            self._storage_policy_id = self._get_storage_policy_id()

        self._STORAGE_POLICY = self._commcell_object._services['GET_STORAGE_POLICY'] % (
            self.storage_policy_id
        )
        self._STORAGE_POLICY_ADVANCED = self._commcell_object._services['GET_STORAGE_POLICY_ADVANCED'] % (
            self.storage_policy_id
        )
        self._storage_policy_properties = None
        self._storage_policy_advanced_properties = None
        self._copies = {}
        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Storage Policy class instance for Storage Policy: "{0}"'
        return representation_string.format(self.storage_policy_name)

    def _get_storage_policy_id(self):
        """Gets the storage policy id asscoiated with the storage policy"""

        storage_policies = StoragePolicies(self._commcell_object)
        return storage_policies.get(self.storage_policy_name).storage_policy_id

    def _get_storage_policy_advanced_properties(self):
        """Gets the advanced storage policy properties of this storage policy.

            Returns:
                dict - dictionary consisting of the advanced properties of this storage policy

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._STORAGE_POLICY_ADVANCED
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_storage_policy_properties(self):
        """Gets the storage policy properties of this storage policy.

            Returns:
                dict - dictionary consisting of the properties of this storage policy

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._STORAGE_POLICY
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_storage_policy_properties(self):
        """Initializes the common properties for the storage policy."""
        self._storage_policy_properties = self._get_storage_policy_properties()
        self._copies = {}

        if 'copy' in self._storage_policy_properties:
            for copy in self._storage_policy_properties['copy']:
                copy_type = copy['copyType']
                active = copy['active']
                copy_id = copy['StoragePolicyCopy']['copyId']
                copy_name = copy['StoragePolicyCopy']['copyName'].lower()
                try:
                    library_name = copy['library']['libraryName']
                except:
                    library_name = None
                copy_precedence = copy['copyPrecedence']
                is_snap_copy = bool(int(copy['isSnapCopy']))
                is_default_copy = bool(int(copy.get('isDefault', 0)))
                temp = {
                    "copyType": copy_type,
                    "active": active,
                    "copyId": copy_id,
                    "libraryName": library_name,
                    "copyPrecedence": copy_precedence,
                    "isSnapCopy": is_snap_copy,
                    "isDefault": is_default_copy
                }
                self._copies[copy_name] = temp

    def has_copy(self, copy_name):
        """Checks if a storage policy copy exists for this storage
            policy with the input storage policy name.

            Args:
                copy_name (str)  --  name of the storage policy copy

            Returns:
                bool - boolean output whether the storage policy copy exists or not

            Raises:
                SDKException:
                    if type of the storage policy copy name argument is not string
        """
        if not isinstance(copy_name, str):
            raise SDKException('Storage', '101')

        return self._copies and copy_name.lower() in self._copies

    def create_secondary_copy(self,
                              copy_name,
                              library_name=None,
                              media_agent_name=None,
                              drive_pool=None,
                              spare_pool=None,
                              tape_library_id=None,
                              drive_pool_id=None,
                              spare_pool_id=None,
                              snap_copy=False,
                              global_policy=None):
        """Creates Synchronous copy for this storage policy

            Args:
                copy_name           (str)   --  copy name to create

                library_name        (str)   --  library name to be assigned

                media_agent_name    (str)   --  media_agent to be assigned

                snap_copy           (bool)  --  boolean on whether copy should be a snap copy
                default: False

                global_policy       (str)   --  name of the global policy to be assigned

            Raises:
                SDKException:
                    if type of inputs in not string

                    if copy with given name already exists

                    if failed to create copy

                    if response received is empty

                    if response is not success
        """
        if global_policy is not None:
            if not (isinstance(copy_name, str) and isinstance(global_policy, str)):
                raise SDKException('Storage', '101')

            if self.has_copy(copy_name):
                err_msg = f'Storage Policy copy "{copy_name}" already exists.'
                raise SDKException('Storage', '102', err_msg)

            if not self._commcell_object.storage_policies.has_policy(global_policy):
                err_msg = f'No Global Storage Policy "{global_policy}" exists.'
                raise SDKException('Storage', '102')

            global_policy = self._commcell_object.storage_policies.get(global_policy)

            global_policy_copy = global_policy.get_copy(list(global_policy.copies.keys())[0])

            is_global_dedupe_policy = global_policy_copy._dedupe_flags.get('enableDeduplication', 0)

            request = {
                       "copyName": copy_name,
                       "storagePolicyCopyInfo": {
                          "copyType": 0,
                          "isDefault": 0,
                          "isMirrorCopy": 0,
                          "isSnapCopy": 0,
                          "numberOfStreamsToCombine": 1,
                          "StoragePolicyCopy": {
                             "_type_": 18,
                             "storagePolicyName": self.storage_policy_name
                          },
                          "retentionRules": {
                             "retainArchiverDataForDays": -1,
                             "retainBackupDataForCycles": 1,
                             "retainBackupDataForDays": 30
                          },
                          "dedupeFlags": {
                              "enableDeduplication": is_global_dedupe_policy,
                              "useGlobalDedupStore": is_global_dedupe_policy
                          },
                           "useGlobalPolicy":{
                               "storagePolicyName": global_policy.name
                           }
                       }
                    }

        else:
            if not (isinstance(copy_name, str) and
                    isinstance(library_name, str) and
                    isinstance(media_agent_name, str)):
                raise SDKException('Storage', '101')

            if self.has_copy(copy_name):
                err_msg = 'Storage Policy copy "{0}" already exists.'.format(copy_name)
                raise SDKException('Storage', '102', err_msg)

            media_agent_id = self._commcell_object.media_agents._media_agents[media_agent_name.lower()]['id']

            snap_copy = int(snap_copy)

            if drive_pool is not None:
                    request = """
                            <App_CreateStoragePolicyCopyReq copyName="{0}">
                                <storagePolicyCopyInfo copyType="0" isDefault="0" isMirrorCopy="0" isSnapCopy="{11}" numberOfStreamsToCombine="1">
                                    <StoragePolicyCopy _type_="18" storagePolicyId="{1}" storagePolicyName="{2}" />
                                    <library _type_="9" libraryId="{3}" libraryName="{4}" />
                                    <mediaAgent _type_="11" mediaAgentId="{5}" mediaAgentName="{6}" />
                                    <drivePool drivePoolId = "{7}" drivePoolName = "{8}"  libraryName = "{4}" />
                                    <spareMediaGroup spareMediaGroupId = "{9}" spareMediaGroupName = "{10}" libraryName = "{4}" />
                                    <retentionRules retainArchiverDataForDays="-1" retainBackupDataForCycles="1" retainBackupDataForDays="30" />
                                </storagePolicyCopyInfo>
                            </App_CreateStoragePolicyCopyReq>
                            """.format(copy_name, self.storage_policy_id, self.storage_policy_name,
                                       tape_library_id, library_name, media_agent_id, media_agent_name,
                                       drive_pool_id, drive_pool, spare_pool_id, spare_pool, snap_copy)

            else:
                library_id = self._commcell_object.disk_libraries._libraries[library_name.lower()]
                request = """
                <App_CreateStoragePolicyCopyReq copyName="{0}">
                    <storagePolicyCopyInfo copyType="0" isDefault="0" isMirrorCopy="0" isSnapCopy="{7}" numberOfStreamsToCombine="1">
                        <StoragePolicyCopy _type_="18" storagePolicyId="{1}" storagePolicyName="{2}" />
                        <library _type_="9" libraryId="{3}" libraryName="{4}" />
                        <mediaAgent _type_="11" mediaAgentId="{5}" mediaAgentName="{6}" />
                        <retentionRules retainArchiverDataForDays="-1" retainBackupDataForCycles="1" retainBackupDataForDays="30" />
                    </storagePolicyCopyInfo>
                </App_CreateStoragePolicyCopyReq>
                """.format(copy_name, self.storage_policy_id, self.storage_policy_name,
                           library_id, library_name, media_agent_id, media_agent_name, snap_copy)

        create_copy_service = self._commcell_object._services['CREATE_STORAGE_POLICY_COPY']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_copy_service, request
        )

        self.refresh()

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = int(response.json()['error']['errorCode'])
                    if error_code != 0:
                        if 'errorMessage' in response.json()['error']:
                            error_message = "Failed to create {0} Storage Policy copy with error \
                            {1}".format(copy_name, str(response.json()['error']['errorMessage']))
                        else:
                            error_message = "Failed to create {0} Storage Policy copy".format(
                                copy_name
                            )
                        raise SDKException('Storage', '102', error_message)

                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def run_content_indexing(self):
        """starts the offline CI job for this storage policy

            Args:
                None

            Returns:
                object - instance of the Job class for this CI job

            Raises:
                SDKException:
                        if type of inputs is not valid

                        if failed to start content indexing job

                        if response received is empty

                        if response is not success
        """
        request_xml = """<TMMsg_CreateTaskReq>
        <taskInfo>
        <associations subclientId="0" storagePolicyId="{0}" applicationId="0" clientName="" backupsetId="0"
        instanceId="0" commCellId="0" clientId="0" subclientName="" mediaAgentId="0" mediaAgentName="" backupsetName=""
        instanceName="" storagePolicyName="{1}" _type_="0" appName="" />
        <task ownerId="1" taskType="1" ownerName="admin" sequenceNumber="0" initiatedFrom="1" policyType="0" taskId="0">
        <taskFlags disabled="0" /></task>
        <subTasks subTaskOperation="1"><subTask subTaskType="1" operationType="4022" />
        <options><backupOpts><mediaOpt>
        <auxcopyJobOption maxNumberOfStreams="0" allCopies="1" useMaximumStreams="1"><mediaAgent mediaAgentId="0"
        _type_="11" mediaAgentName="" />
        </auxcopyJobOption></mediaOpt></backupOpts><adminOpts>
        <contentIndexingOption fileAnalytics="0" subClientBasedAnalytics="0" reanalyze="0" />
        </adminOpts>
        <restoreOptions><virtualServerRstOption isBlockLevelReplication="0" /><commonOptions syncRestore="0" />
        </restoreOptions></options></subTasks>
        </taskInfo></TMMsg_CreateTaskReq>""".format(self._storage_policy_id, self._storage_policy_name)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                else:
                    raise SDKException('Storage', '102', 'Unable to get job id for CI job')
            else:
                raise SDKException('Response', '102', 'Empty response')
        else:
            raise SDKException('Response', '101')

    def enable_content_indexing(
            self,
            cloud_id,
            include_doc_type=None,
            max_doc_size=None,
            min_doc_size=None,
            exclude_doc_type=None):
        """configures offline CI for this storage policy

                Args:

                    cloud_id            (str)   --  cloud id of the search engine

                    include_doc_type    (str)   --  include document types for content indexing

                        Example : "*.csv,*.ppt"

                    exclude_doc_type    (str)   --  exclude document types for content indexing

                        Example : "*.py,*.txt"

                    max_doc_size        (str)   --  maximum document size for CI in KB

                    min_doc_size        (str)   --  minimum document size for CI in KB

                Returns:
                    None

                Raises:

                    SDKException:
                            if type of inputs is not valid

                            if failed to configure content indexing

                            if response received is empty

                            if response is not success
        """
        if not isinstance(cloud_id, str):
            raise SDKException('Storage', '101')

        if include_doc_type is None:
            include_doc_type = "*.bmp,*.csv,*.doc,*.docx,*.dot,*.eml,*.htm,*.html,*.jpeg,*.jpg,*.log,*.msg,*.odg," \
                               "*.odp,*.ods,*.odt,*.pages,*.pdf,*.png,*.ppt,*.pptx,*.rtf,*.txt,*.xls,*.xlsx,*.xmind,*.xml"
        if max_doc_size is None:
            max_doc_size = "51200"

        if min_doc_size is None:
            min_doc_size = "0"

        if exclude_doc_type is None:
            exclude_doc_type = ""

        request_xml = """<EVGui_ContentIndexingControlReq operation="16"><header localeId="0" userId="0"/>
        <ciProps archGroupId="{0}" calendarId="1" cloudId="{1}" contentIndexDataOver="0" dayNumber="0" deferredDays="0"
         enable="1" entityIds="" excludeDocTypes="{5}" filterSelected="1" flags="0"
         includeDocTypes="{2}" indexType="0" jobsOlderThan="0"
         maxDocSizeKB="{3}" minDocSizeKB="{4}" numPeriod="1" retentionDays="-1" sourceCopyId="0" startTime="0"
         synchronizeOn="0" type="0"/></EVGui_ContentIndexingControlReq>"""\
            .format(self._storage_policy_id, cloud_id, include_doc_type, max_doc_size, min_doc_size, exclude_doc_type)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = int(response.json()['error']['errorCode'])
                    if error_code != 1:
                        error_message = "Failed to enable content indexing for this storage policy"
                        raise SDKException('Storage', '102', error_message)
                else:
                    raise SDKException('Response', '102', 'No success error code found in response')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_entity_extraction(self, entity_details, entity_names, ca_client_name):
        """configures offline CI entity extraction for given subclient id's on this storage policy

                Args:
                    entity_details     (list)     --  List of subclient to configure for Entity Extraction

                    Format : [[clientname,agent type,backup set name,subclient name]]

                    entity_names         (list)   --  list of entity names to be configured for Entity Extraction

                    Example : [Email,SSN]

                    ca_client_name       (str)    --  client name where Content Analyzer package is installed

                Raises:
                    SDKException:
                        if type of inputs is not valid

                        if failed to configure EE

                        if response received is empty

                        if response is not success
        """
        if not (isinstance(entity_details, list) and isinstance(entity_names, list)):
            raise SDKException('Storage', '101')
        if not isinstance(ca_client_name, str):
            raise SDKException('Storage', '101')
        request_xml = """<EVGui_SetEntityExtractionListReq archGroupId="{0}">
        <entityExtraction isConfigured="1">""".format(self._storage_policy_id)
        for subclient in entity_details:
            client_name = subclient[0]
            app_name = subclient[1]
            backup_set_name = subclient[2]
            subclient_name = subclient[3]
            client_obj = self._commcell_object.clients.get(client_name)
            agent_obj = client_obj.agents.get(app_name)
            backup_set_obj = agent_obj.backupsets.get(backup_set_name)
            subclient_obj = backup_set_obj.subclients.get(subclient_name)
            if subclient_obj.storage_policy.lower() != self._storage_policy_name.lower():
                err_msg = 'Subclient "{0}" is not a part of this storage policy'.format(subclient_name)
                raise SDKException('Storage', '102', err_msg)
            subclient_prop = subclient_obj.properties
            request_xml = request_xml + """<appList appOperation="0" appTypeId="{0}" archGroupId="0"
                backupSetId="{1}" clientId="{2}" instanceId="{3}" subClientId="{4}"/>""".format(
                subclient_prop['subClientEntity']['applicationId'],
                subclient_prop['subClientEntity']['backupsetId'],
                subclient_prop['subClientEntity']['clientId'],
                subclient_prop['subClientEntity']['instanceId'],
                subclient_prop['subClientEntity']['subclientId'],
            )

        for entity in entity_names:
            entity_obj = self._commcell_object.activate.entity_manager().get(entity)
            request_xml = request_xml + """<entities enabled="1" entityId="{0}" entityName="{1}"/>"""\
                .format(entity_obj.entity_id, entity)

        client_obj = self._commcell_object.clients.get(ca_client_name)
        request_xml = request_xml + """<extractingClientList enabled="1">
        <eeClient clientId="{0}" clientName="{1}"/>
        </extractingClientList></entityExtraction></EVGui_SetEntityExtractionListReq>"""\
            .format(client_obj.client_id, ca_client_name)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json()['errorCode'])
                    if error_code != 0:
                        error_message = "Failed to enable entity extraction for this storage policy"
                        raise SDKException('Storage', '102', error_message)
                else:
                    raise SDKException('Response', '102', 'No success error code found in response')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def create_snap_copy(self,
                         copy_name,
                         is_mirror_copy,
                         is_snap_copy,
                         library_name,
                         media_agent_name,
                         source_copy,
                         provisioning_policy=None,
                         resource_pool=None,
                         is_replica_copy=None,
                         **kwargs):
        """Creates Snap copy for this storage policy

            Args:
                copy_name           (str)   --  copy name to create

                is_mirror_copy      (bool)   --  if true then copyType will be Mirror

                is_snap_copy        (bool)   --  if true then copyType will be Snap

                library_name        (str)   --  library name to be assigned

                media_agent_name    (str)   --  media_agent to be assigned

                source_copy         (str)   --  Name of the Source Copy for this copy

                provisioning_policy (str)   --  Name of the provisioning Policy to add
                default : None

                resource_pool       (str)   --  Name of the resource pool to add
                default : None

                is_replica_copy     (bool)   --  if true then Replica Copy will be created
                default : None

                is_c2c_target       (bool)   -- if true then NetApp Cloud target copy will be created 
                default : False

                job_retention       (bool)  -- if true job based retention will be set
                default : False

            Raises:
                SDKException:
                    if type of inputs in not string

                    if copy with given name already exists

                    if failed to create copy

                    if response received is empty

                    if response is not success
        """
        if not (isinstance(copy_name, str) and
                isinstance(library_name, str) and
                isinstance(media_agent_name, str)):
            raise SDKException('Storage', '101')

        if self.has_copy(copy_name):
            err_msg = 'Storage Policy copy "{0}" already exists.'.format(copy_name)
            raise SDKException('Storage', '102', err_msg)

        if is_replica_copy:
            arrayReplicaCopy = "1"
            useOfflineReplication = "1"
        else:
            arrayReplicaCopy = "0"
            useOfflineReplication = "0"
        if is_mirror_copy:
            is_mirror_copy = 1
        else:
            is_mirror_copy = 0
        if is_snap_copy:
            is_snap_copy = 1
        else:
            is_snap_copy = 0
        if provisioning_policy is None:
            provisioning_policy = ""
            resource_pool = ""

        is_c2c_target = kwargs.get('is_c2c_target', False)
        isNetAppSnapCloudTargetCopy = 1 if is_c2c_target else 0

        job_based_retention = kwargs.get('job_based_retention', False)
        job_retention = 1 if job_based_retention else 0
        request_xml = """
                    <App_CreateStoragePolicyCopyReq copyName="{0}">
                        <storagePolicyCopyInfo active="1" isMirrorCopy="{1}" isSnapCopy="{2}" provisioningPolicyName="{3}">
                            <StoragePolicyCopy _type_="18" copyName="{0}" storagePolicyName="{4}" />
                            <extendedFlags arrayReplicaCopy="{5}" isNetAppSnapCloudTargetCopy="{12}" useOfflineArrayReplication="{6}" />
                            <library _type_="9" libraryName="{7}" />
                            <mediaAgent _type_="11" mediaAgentName="{8}" />
                            <spareMediaGroup _type_="67" libraryName="{7}" />
                            <retentionRules jobs="8" retainArchiverDataForDays="-1" retainBackupDataForCycles="5" retainBackupDataForDays="1">
                            <retentionFlags jobBasedRetention="{11}" />
                            </retentionRules>
                            <sourceCopy _type_="18" copyName="{9}" storagePolicyName="{4}" />
                            <resourcePoolsList operation="1" resourcePoolName="{10}" />
                        </storagePolicyCopyInfo>
                    </App_CreateStoragePolicyCopyReq>
                    """.format(copy_name, is_mirror_copy, is_snap_copy, provisioning_policy,
                               self.storage_policy_name, arrayReplicaCopy, useOfflineReplication,
                               library_name, media_agent_name, source_copy, resource_pool, job_retention, isNetAppSnapCloudTargetCopy)

        create_copy_service = self._commcell_object._services['CREATE_STORAGE_POLICY_COPY']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_copy_service, request_xml
        )

        self.refresh()

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = int(response.json()['error']['errorCode'])
                    if error_code != 0:
                        if 'errorMessage' in response.json()['error']:
                            error_message = "Failed to create {0} Storage Policy copy with error \
                            {1}".format(copy_name, str(response.json()['error']['errorMessage']))
                        else:
                            error_message = "Failed to create {0} Storage Policy copy".format(
                                copy_name
                            )
                        raise SDKException('Storage', '102', error_message)

                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def delete_secondary_copy(self, copy_name):
        """Deletes the copy associated with this storage policy

            Args:
                copy_name   (str)   --  copy name to be deleted

            Raises:
                SDKException:
                    if type of input parameters is not string

                    if storage policy copy doesn't exist with given name

                    if failed to delete storage policy copy

                    if response received is empty

                    if response is not success
        """
        if not isinstance(copy_name, str):
            raise SDKException('Storage', '101')
        else:
            copy_name = copy_name.lower()

        if not self.has_copy(copy_name):
            err_msg = 'Storage Policy copy "{0}" doesn\'t exists.'.format(copy_name)
            raise SDKException('Storage', '102', err_msg)

        delete_copy_service = self._commcell_object._services['DELETE_STORAGE_POLICY_COPY']

        request_xml = """
        <App_DeleteStoragePolicyCopyReq>
            <archiveGroupCopy _type_="18" copyId="{0}" copyName="{1}" storagePolicyId="{2}" storagePolicyName="{3}" />
        </App_DeleteStoragePolicyCopyReq>
        """.format(self._copies[copy_name]['copyId'], copy_name, self.storage_policy_id,
                   self.storage_policy_name)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', delete_copy_service, request_xml
        )

        self.refresh()

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = int(response.json()['error']['errorCode'])
                    if error_code != 0:
                        error_message = "Failed to delete {0} Storage Policy copy".format(
                            copy_name
                        )
                        raise SDKException('Storage', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def create_selective_copy(self,
                              copy_name,
                              library_name,
                              media_agent_name,
                              sel_freq,
                              first_or_last_full,
                              backups_from,
                              daystartson=None):
        """Creates Selective copy for this storage policy

            Args:
                copy_name           (str)   --  copy name to create
                library_name        (str)   --  library name to be assigned
                media_agent_name    (str)   --  media_agent to be assigned
                drive_pool etc are for tape library

                sel_freq            (str) -- {all,hourly,daily,weekly,monthly,quaterly,half-year,year}
                first_or_last_full  (str) -- {FirstFull, LastFull, LastFullWait}
                backups_from        (str) -- {start date in yyyy-mm-dd format to pick jobs from this date}

            Raises:
                SDKException:
                    if type of inputs in not string

                    if copy with given name already exists

                    if failed to create copy

                    if response received is empty

                    if response is not success
        """
        if not (isinstance(copy_name, str) and
                isinstance(library_name, str) and
                isinstance(media_agent_name, str)):
            raise SDKException('Storage', '101')

        if self.has_copy(copy_name):
            err_msg = 'Storage Policy copy "{0}" already exists.'.format(copy_name)
            raise SDKException('Storage', '102', err_msg)

        media_agent_id = self._commcell_object.media_agents._media_agents[media_agent_name.lower()]['id']

        selective_copy_freq = {'all': 2, 'hourly': 262144, 'daily': 524288, 'weekly': 4, 'monthly': 8,
                               'quarterly': 16, 'halfyearly': 32, 'yearly': 64, 'advanced': 16777216
                               }
        week_starts_on = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
                          'Friday': 5, 'Saturday': 6
                          }

        selective_rule = selective_copy_freq[sel_freq]
        copyflags = ""
        if first_or_last_full == "LastFull":
            copyflags = """<copyFlags lastFull = "1" />"""
        elif first_or_last_full == "LastFullWait":
            copyflags = """<copyFlags lastFull = "1" lastFullWait="1" />"""

        dsostr = ""
        if (sel_freq == 'daily' or sel_freq == 'hourly') and daystartson is not None \
                and isinstance(daystartson, dict):
            dsostr = """
                        <dayStartsAt amOrPm = "{3}"> 
                        <dayStartsHoursMinutes hours="{0}" minutes = "{1}"  seconds= "{2}" />
                        </dayStartsAt> 
                     """.format(daystartson["hours"], daystartson["minutes"], daystartson["seconds"],
                                daystartson["ampm"])

        day_starts = ""
        if sel_freq == 'weekly':
            if daystartson is not None:
                day_starts = """ weekDayStartsOn="{0}" """.format(week_starts_on[daystartson])
            else:
                day_starts = """ weekDayStartsOn="{0}" """.format(week_starts_on['Friday'])

        # monthStartsOn
        if sel_freq == 'monthly':
            if daystartson is not None:
                day_starts = """ monthStartsOn="{0}" """.format(daystartson)
            else:
                day_starts = """ monthStartsOn="{}" """.format(1)

        library_id = self._commcell_object.disk_libraries._libraries[library_name.lower()]
        request_xml = str("""<App_CreateStoragePolicyCopyReq copyName="{0}">
                <storagePolicyCopyInfo copyType="2" isDefault="0" isMirrorCopy="0" isSnapCopy="0" numberOfStreamsToCombine="1">
                    <StoragePolicyCopy _type_="18" storagePolicyId="{1}" storagePolicyName="{2}" />
                    <library _type_="9" libraryId="{3}" libraryName="{4}" />
                    <mediaAgent _type_="11" mediaAgentId="{5}" mediaAgentName="{6}" />
                    <retentionRules retainArchiverDataForDays="-1" retainBackupDataForCycles="100" retainBackupDataForDays="150" />
                    <startTime  timeValue = "{7}" />
                    <selectiveCopyRules selectiveRule="{8}" {10} > {9} </selectiveCopyRules> """ + copyflags +
                              """</storagePolicyCopyInfo>
                          </App_CreateStoragePolicyCopyReq>""").format(copy_name, self.storage_policy_id,
                                                                       self.storage_policy_name,
                                                                       library_id, library_name, media_agent_id,
                                                                       media_agent_name, backups_from,
                                                                       selective_rule, dsostr, day_starts)
        create_copy_service = self._commcell_object._services['CREATE_STORAGE_POLICY_COPY']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_copy_service, request_xml)

        self.refresh()

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = int(response.json()['error']['errorCode'])
                    if error_code != 0:
                        if 'errorMessage' in response.json()['error']:
                            error_message = "Failed to create {0} Storage Policy copy with error \
                            {1}".format(copy_name, str(response.json()['error']['errorMessage']))
                        else:
                            error_message = "Failed to create {0} Storage Policy copy".format(
                                copy_name
                            )
                        raise SDKException('Storage', '102', error_message)

                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def copies(self):
        """Treats the storage policy copies as a read-only attribute"""
        return self._copies

    @property
    def storage_policy_id(self):
        """Treats the storage policy id as a read-only attribute."""
        return self._storage_policy_id

    @property
    def name(self):
        """Returns the Storage Policy display name"""
        return self._storage_policy_properties['storagePolicy']['storagePolicyName']

    @property
    def storage_policy_name(self):
        """Treats the storage policy name as a read-only attribute."""
        return self._storage_policy_name

    @property
    def description(self):
        """Returns the Storage Policy Description Field"""
        if self._storage_policy_advanced_properties is None:
            self._storage_policy_advanced_properties = self._get_storage_policy_advanced_properties()
        return self._storage_policy_advanced_properties.get('policies',[{}])[0].get('description')

    def get_copy_precedence(self, copy_name):
        """ returns the copy precedence value associated with the copy name

            Args:
                copy_name           (str)   --  Storage copy name

            Returns:
                copy_precedence     (int)   --  Copy precedence number of
                storage copy

            Raises:
                Exception:
                    if unable to find the given copy name

        """
        policy_copies = self.copies
        if policy_copies.get(copy_name):
            if policy_copies[copy_name].get('copyPrecedence'):
                return policy_copies[copy_name]['copyPrecedence']
        raise SDKException(
            'Storage',
            '102',
            'Failed to get copy precedence from policy')

    def update_snapshot_options(self, **options):
        """
        Method for Updating Storage Policy Snapshot Options like Backup Copy and Snapshot Catalog

        Args:
            Available Snapshot Options:

            enable_backup_copy               (bool)   --  Enables backup copy if the value is True

            source_copy_for_snap_to_tape     (str)    --  Source Copy name for backup copy

            enable_snapshot_catalog          (bool)   --  Enables Snapshot Catalog if value is True

            source_copy_for_snapshot_catalog (str)    --  Source Copy name for Snapshot Catalog

            is_ocum                          (bool)   --  True if Storage policy is enabled with
                                                          ocum server
            enable_selective_copy                 (int)   -- Enable selective copy option based on input value

        """
        enable_backup_copy = options['enable_backup_copy']
        enable_snapshot_catalog = options['enable_snapshot_catalog']

        if options['is_ocum']:
            if enable_backup_copy and enable_snapshot_catalog:
                defferred_catalog_value = backup_copy_value = 16
            else:
                defferred_catalog_value = backup_copy_value = 3
        else:
            if enable_backup_copy:
                defferred_catalog_value = 16
                backup_copy_value = 3
            else:
                defferred_catalog_value = backup_copy_value = 3

        if options['source_copy_for_snap_to_tape'] is not None:
            source_copy_for_snap_to_tape_id = self._copies[options['source_copy_for_snap_to_tape'].lower()]['copyId']
        else:
            source_copy_for_snap_to_tape_id = 0
        if options['source_copy_for_snapshot_catalog'] is not None:
            source_copy_for_snapshot_catalog_id = self._copies[options['source_copy_for_snapshot_catalog'].lower(
            )]['copyId']
        else:
            source_copy_for_snapshot_catalog_id = 0

        selective_type = options.get('enable_selective_copy', 0)

        update_snapshot_tab_service = self._commcell_object._services['EXECUTE_QCOMMAND']

        request_xml = """
                    <EVGui_SetSnapOpPropsReq deferredCatalogOperation="{0}" snapshotToTapeOperation="{1}">
                        <header localeId="0" userId="0" />
                        <snapshotToTapeProps archGroupId="{2}" calendarId="1" dayNumber="0" deferredDays="0"
                            enable="{3}" flags="0" infoFlags="0" numOfReaders="0" numPeriod="1"
                            sourceCopyId="{4}" startTime="0" type="{7}" />
                        <deferredCatalogProps archGroupId="{2}" calendarId="1" dayNumber="0" deferredDays="0"
                            enable="{5}" flags="0" infoFlags="0" numOfReaders="0" numPeriod="1"
                            sourceCopyId="{6}" startTime="0" type="0" />
                    </EVGui_SetSnapOpPropsReq>
        """.format(defferred_catalog_value, backup_copy_value, self.storage_policy_id,
                   int(enable_backup_copy), source_copy_for_snap_to_tape_id,
                   int(enable_snapshot_catalog), source_copy_for_snapshot_catalog_id, selective_type)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', update_snapshot_tab_service, request_xml
        )

        self.refresh()

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = int(response.json()['error']['errorCode'])
                    if error_code != 1:
                        error_message = "Failed to Update {0} Storage Policy".format(
                            self.storage_policy_name
                        )
                        raise SDKException('Storage', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def run_backup_copy(self):
        """
        Runs the backup copy from Commcell for the given storage policy

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
                        "storagePolicyName": self.storage_policy_name
                    }
                ],
                "task": {
                    "initiatedFrom": 2,
                    "taskType": 1,
                    "policyType": 3,
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
                    raise SDKException('Storage', '106', o_str)
                else:
                    raise SDKException('Storage', '106', 'Failed to run the backup copy job')
            else:
                raise SDKException('Response', '106')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def modify_dynamic_stream_allocation(self, enable=True):
        """
        Modifies the DSA option for the Storage Policy
            Args:

                    enable      (bool)  --   False - Disable DSA
                                             True - Enable DSA
        """
        request_xml = '''<App_UpdateStoragePolicyReq>
                       <StoragePolicy>
                           <storagePolicyName>{0}</storagePolicyName>
                       </StoragePolicy>
                       <flag>
                           <distributeDataEvenlyAmongStreams>{1}</distributeDataEvenlyAmongStreams>
                       </flag>
                       </App_UpdateStoragePolicyReq>
                       '''.format(self.storage_policy_name, int(enable))
        self._commcell_object.qoperation_execute(request_xml)

    def run_snapshot_cataloging(self):
        """
        Runs the deferred catalog job from Commcell for the given storage policy

        Args:
                None

        Returns:
                object - instance of the Job class for this snapshot cataloging job

        Raises:
            SDKException:

                    if snapshot cataloging job failed

                    if response is empty

                    if response is not success
        """

        request_json = {
            "taskInfo": {
                "associations": [
                    {
                        "storagePolicyName": self.storage_policy_name
                    }
                ],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0,
                    "taskFlags": {
                        "isEdgeDrive": False,
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4043
                        },
                        "options": {
                            "backupOpts": {
                                "backupLevel": 2,
                                "dataOpt": {
                                    "useCatalogServer": True,
                                    "enforceTransactionLogUsage": False
                                }
                            }
                        }
                    }
                ]
            }
        }

        snapshot_catalog = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', snapshot_catalog, request_json)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Deferred catalog job failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Storage', '107', o_str)
                else:
                    raise SDKException('Storage', '107', 'Failed to run the deferred catalog job')
            else:
                raise SDKException('Response', '107')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def storage_policy_properties(self):
        """Returns the storage policy properties

            dict - consists of storage policy properties
        """
        return self._storage_policy_properties

    @property
    def storage_policy_advanced_properties(self):
        """Returns the  storage policy advanced properties

            dict - consists of storage policy advanced properties
        """
        if self._storage_policy_advanced_properties is None:
            self._storage_policy_advanced_properties = self._get_storage_policy_advanced_properties()
        return self._storage_policy_advanced_properties

    @property
    def library_name(self):
        """Treats the library name as a read-only attribute."""
        primary_copy = self._storage_policy_properties.get('copy')
        if 'library' in primary_copy[0]:
            library = primary_copy[0].get('library', {})
            return library.get('libraryName')

    @property
    def library_id(self):
        """Treats the library id as a read-only attribute."""
        primary_copy = self._storage_policy_properties.get('copy')
        if 'library' in primary_copy[0]:
            library = primary_copy[0].get('library', {})
            return library.get('libraryId')

    @property
    def aux_copies(self):
        """
        Returns the list of all aux copies in the policy
        Returns:
            list - list of all aux copies in the storage policy
        """
        aux_copies = []
        for _copy, value in self.copies.items():
            if not value['isSnapCopy'] and _copy != 'primary':
                aux_copies.append(_copy)
        return aux_copies

    @property
    def snap_copy(self):
        """
        Returns the name of the snap copy
        Returns:
            str - name of the snap copy
        """
        snap_copy = None
        for _copy, value in self.copies.items():
            if value['isSnapCopy']:
                snap_copy = _copy
        return snap_copy

    def run_aux_copy(self, storage_policy_copy_name=None,
                     media_agent=None, use_scale=True, streams=0,
                     all_copies=True, total_jobs_to_process=1000, schedule_pattern=None):
        """Runs the aux copy job from the commcell.
            Args:

                storage_policy_copy_name (str)  --  name of the storage policy copy

                media_agent              (str)  --  name of the media agent

                use_scale                (bool) --  use Scalable Resource Management (True/False)

                streams                  (int)  --  number of streams to use

                all_copies               (bool) -- run auxcopy job on all copies or select copy
                                                   (True/False)

                total_jobs_to_process    (int)  -- Total number jobs to process for the auxcopy job

            Returns:
                object - instance of the Job class for this aux copy job

            Raises:
                SDKException:
                    if type of the  argument is not string

                    if aux copy job failed

                    if response is empty

                    if response is not success
        """
        if not (isinstance(total_jobs_to_process, int) and
                isinstance(streams, int)):
            raise SDKException('Storage', '101')

        use_max_streams = True
        if streams != 0:
            use_max_streams = False

        if storage_policy_copy_name is not None:
            all_copies = False
            if not media_agent:
                media_agent = "&lt;ANY MEDIAAGENT&gt;"
            if not (isinstance(storage_policy_copy_name, str) and
                    isinstance(media_agent, str)):
                raise SDKException('Storage', '101')
        else:
            if all_copies is False:
                raise SDKException('Storage', '110')
            storage_policy_copy_name = ""
            media_agent = ""

        request_json = {
            "taskInfo": {
                "associations": [
                    {
                        "copyName": storage_policy_copy_name,
                        "storagePolicyName": self.storage_policy_name
                    }
                ],
                "task": {
                    "initiatedFrom": 2,
                    "taskType": 1,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4003
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "maxNumberOfStreams": streams,
                                        "useMaximumStreams": use_max_streams,
                                        "useScallableResourceManagement": use_scale,
                                        "totalJobsToProcess": total_jobs_to_process,
                                        "allCopies": all_copies,
                                        "mediaAgent": {
                                            "mediaAgentName": media_agent
                                        }
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        aux_copy = self._commcell_object._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', aux_copy, request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)

                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

                else:
                    raise SDKException('Storage', '102', 'Failed to run the aux copy job')
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the StoragePolicy."""
        self._initialize_storage_policy_properties()
        self._storage_policy_advanced_properties = None

    def seal_ddb(self, copy_name):
        """
        Seals the deduplication database

            Args:
                copy_name   (str)   --  name of the storage policy copy

            Raises:
                SDKException:
                    if type of input parameters is not string
        """
        if not isinstance(copy_name, str):
            raise SDKException('Storage', '101')

        request_xml = """
        <App_SealSIDBStoreReq>
            <archiveGroupCopy>
                <copyName>{0}</copyName>
                <storagePolicyName>{1}</storagePolicyName>
            </archiveGroupCopy>
        </App_SealSIDBStoreReq>

        """.format(copy_name, self.storage_policy_name)
        self._commcell_object._qoperation_execute(request_xml)

    def update_transactional_ddb(self, update_value, copy_name, media_agent_name):
        """
        Updates TransactionalDDB option on the deduplication database

            Args:
                update_value    (bool)   --   enable(True)/disable(False)

                copy_name       (str)   --   name of the associated copy

                media_agent_name(str)   --   name of the media agent

            Raises:
                SDKException:
                    if type of input parameters is not string
        """
        if not (isinstance(copy_name, str) and isinstance(media_agent_name, str)):
            raise SDKException('Storage', '101')

        request_xml = """
        <App_UpdateStoragePolicyCopyReq >
            <storagePolicyCopyInfo >
                <StoragePolicyCopy>
                    <copyName>{0}</copyName>
                    <storagePolicyName>{1}</storagePolicyName>
                </StoragePolicyCopy>
                <DDBPartitionInfo>
                    <maInfoList>
                        <mediaAgent>
                            <mediaAgentName>{2}</mediaAgentName>
                        </mediaAgent>
                            </maInfoList>
                            <sidbStoreInfo>
                                <sidbStoreFlags>
                            <enableTransactionalDDB>{3}</enableTransactionalDDB>
                        </sidbStoreFlags>
                            </sidbStoreInfo>
                    </DDBPartitionInfo>
           </storagePolicyCopyInfo>
        </App_UpdateStoragePolicyCopyReq>
        """.format(copy_name, self.storage_policy_name, media_agent_name, int(update_value))

        self._commcell_object._qoperation_execute(request_xml)

    def create_dedupe_secondary_copy(self, copy_name, library_name,
                                     media_agent_name, path, ddb_media_agent,
                                     dash_full=None,
                                     source_side_disk_cache=None,
                                     software_compression=None):
        """Creates Synchronous copy for this storage policy

            Args:
                copy_name               (str)   --  copy name to create

                library_name            (str)   --  library name to be assigned

                media_agent_name        (str)   --  media_agent to be assigned

                path                    (str)   --  path where deduplication store is to be hosted

                ddb_media_agent         (str)   --  media agent name on which deduplication store
                                                    is to be hosted

                dash_full               (bool)  --  enable DASH full on deduplication store (True/False)
                Default None

                source_side_disk_cache  (bool)  -- enable source side disk cache (True/False)
                Default None

                software_compression    (bool)  -- enable software compression (True/False)
                Default None

            Raises:
                SDKException:
                    if type of inputs in not string

                    if copy with given name already exists

                    if failed to create copy

                    if response received is empty

                    if response is not success
        """
        if not (isinstance(copy_name, str) and
                isinstance(library_name, str) and
                isinstance(path, str) and
                isinstance(ddb_media_agent, str) and
                isinstance(media_agent_name, str)):
            raise SDKException('Storage', '101')

        if dash_full is None:
            dash_full = "2"
        if source_side_disk_cache is None:
            source_side_disk_cache = "2"
        if software_compression is None:
            software_compression = "2"

        if self.has_copy(copy_name):
            err_msg = 'Storage Policy copy "{0}" already exists.'.format(copy_name)
            raise SDKException('Storage', '102', err_msg)

        library_id = self._commcell_object.disk_libraries.get(library_name).library_id
        media_agent_id = self._commcell_object.media_agents._media_agents[media_agent_name]['id']

        request_xml = """
        <App_CreateStoragePolicyCopyReq copyName="{0}">
            <storagePolicyCopyInfo copyType="0" isDefault="0">
                <StoragePolicyCopy _type_="18" storagePolicyId="{1}" storagePolicyName="{2}" />
                <library _type_="9" libraryId="{3}" libraryName="{4}" />
                <mediaAgent _type_="11" mediaAgentId="{5}" mediaAgentName="{6}" />
                <copyFlags auxCopyReencryptData="0" />
                <dedupeFlags enableDeduplication="1" enableDASHFull="{9}" enableSourceSideDiskCache="{10}"/>
                <retentionRules retainArchiverDataForDays="-1" retainBackupDataForCycles="1" retainBackupDataForDays="30" />
                <DDBPartitionInfo>
                    <maInfoList>
                        <mediaAgent mediaAgentName="{8}"/>
                        <subStoreList>
                            <diskFreeThresholdMB>5120</diskFreeThresholdMB>
                            <diskFreeWarningThreshholdMB>10240</diskFreeWarningThreshholdMB>
                            <accessPath path="{7}"/>
                        </subStoreList>
                    </maInfoList>
                    <sidbStoreInfo>
                        <operation>1</operation>
                        <copyName>{0}</copyName>
                        <sidbStoreFlags enableSoftwareCompression="{11}"/>
                    </sidbStoreInfo>
                </DDBPartitionInfo>

            </storagePolicyCopyInfo>
        </App_CreateStoragePolicyCopyReq>
        """.format(copy_name, self._storage_policy_id, self.storage_policy_name,
                   library_id, library_name, media_agent_id, media_agent_name,
                   path, ddb_media_agent, int(dash_full),
                   int(source_side_disk_cache), int(software_compression))

        create_copy_service = self._commcell_object._services['CREATE_STORAGE_POLICY_COPY']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_copy_service, request_xml
        )

        self.refresh()

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = int(response.json()['error']['errorCode'])
                    if error_code != 0:
                        if 'errorMessage' in response.json()['error']:
                            error_message = "Failed to create {0} Storage Policy copy with error \
                            {1}".format(copy_name, str(response.json()['error']['errorMessage']))
                        else:
                            error_message = "Failed to create {0} Storage Policy copy".format(
                                copy_name
                            )

                        raise SDKException('Storage', '102', error_message)

                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def run_ddb_verification(self,
                             copy_name,
                             ver_type,
                             ddb_ver_level,
                             use_scalable=True,
                             orphan_chunk_listing=False):
        """
        Runs DDB verification job

            Args:
                copy_name       (str)   --  name of the copy which is associated with the DDB store

                ver_type        (str)   --  backup level (Full/Incremental)

                ddb_ver_level   (str)   --  DDB verification type
                                            (DDB_VERIFICATION/ DDB_AND_DATA_VERIFICATION /
                                            QUICK_DDB_VERIFICATION/ DDB_DEFRAGMENTATION)

                use_scalable    (bool)  --  True/False to use Scalable Resource Allocation
                                            Default: True

                orphan_chunk_listing (bool) --  True/False to run orphan chunk listing phase during DDB Defragmentation

            Returns:
                object - instance of the Job class for this DDB verification job

            Raises:
                SDKException:
                    if type of input parameters is not string

                    if job failed

                    if response is empty

                    if response is not success
        """
        if not (isinstance(copy_name, str) and
                isinstance(ver_type, str) and
                isinstance(ddb_ver_level, str)):
            raise SDKException('Storage', '101')
        run_defrag = False
        if ddb_ver_level == 'DDB_DEFRAGMENTATION':
            run_defrag = True
        request = {
            "taskInfo": {
                "associations": [
                    {
                        "copyName": copy_name, "storagePolicyName": self.storage_policy_name
                    }
                ], "task": {
                    "taskType": 1,
                    "initiatedFrom": 1,
                    "policyType": 0,
                    "taskId": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                }, "subTasks": [
                    {
                        "subTaskOperation": 1, "subTask": {
                            "subTaskType": 1, "operationType": 4007
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "maxNumberOfStreams": 0,
                                        "allCopies": True,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": use_scalable,
                                        "mediaAgent": {
                                            "mediaAgentName": ""
                                        }
                                    }
                                }
                            }, "adminOpts": {
                                "archiveCheckOption": {
                                    "ddbVerificationLevel": ddb_ver_level,
                                    "jobsToVerify": 0,
                                    "allCopies": True,
                                    "backupLevel": ver_type,
                                    "ocl": orphan_chunk_listing,
                                    "runDefrag": run_defrag
                                }
                            }
                        }
                    }
                ]
            }
        }
        data_verf = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', data_verf, request
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'DDB verification job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                else:
                    raise SDKException('Storage', '109')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def run_data_verification(self, media_agent_name='', copy_name='', streams=0,
                              jobs_to_verify='NEW', use_scalable=True, schedule_pattern=None, **kwargs):
        """Runs Data verification job

        Args:
            media_agent_name    (str)  : name of the mediaAgent to use for data reading

            copy_name           (str)  : name of Copy
                                         (default - verifies jobs on all copies)

            streams             (int)  : number of streams to use
                                         (default - use Maximum)

            jobs_to_verify      (str)  : jobs to be Verified
                                         (NEW/ VERF_EXPIRED/ ALL)

            use_scalable       (bool) : True/False to use Scalable Resource Allocation
                                         (default - True)

            kwargs              (dict) : optional arguments
                Available kwargs Options:
                    job_description     (str): Description for Job

        Returns:
            object - instance of the Job class for this Data Verification Job

            errorMessage - If Data Verification Job fails to Start
        """
        if not (isinstance(copy_name, str) and isinstance(jobs_to_verify, str)
                and isinstance(media_agent_name, str) and isinstance(streams, int)):
            raise SDKException('Storage', '101')

        if jobs_to_verify.upper() == 'NEW':
            jobs_to_verify = 'NEWLY_AVAILABLE'
        elif jobs_to_verify.upper() == 'VERF_EXPIRED':
            jobs_to_verify = 'VERIFICATION_EXP'
        elif jobs_to_verify.upper() == 'ALL':
            jobs_to_verify = 'BOTH_NEWLY_AVAILABLE_AND_VERIFICATION_EXP'

        request = {
            "taskInfo": {
                "associations": [
                    {
                        "copyName": copy_name,
                        "storagePolicyName": self.storage_policy_name
                    }
                ],
                "task": {},
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4007
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "maxNumberOfStreams": streams,
                                        "useMaximumStreams": not bool(streams),
                                        "useScallableResourceManagement": use_scalable,
                                        "mediaAgent": {
                                            "mediaAgentName": media_agent_name
                                        }
                                    }
                                }
                            },
                            "adminOpts": {
                                "archiveCheckOption": {
                                    "jobsToVerify": jobs_to_verify,
                                }
                            },
                            "commonOpts": {
                                "jobDescription": kwargs.get('job_description','')
                            }
                        }
                    }
                ]
            }
        }

        if schedule_pattern:
            request["taskInfo"]["task"] = {"taskType": 2}
            request = SchedulePattern().create_schedule(request, schedule_pattern)

        data_verf = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', data_verf, request
        )
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Data verification Request failed. Error: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])
                else:
                    raise SDKException('Storage', '109')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def move_dedupe_store(self,
                          copy_name,
                          dest_path,
                          src_path,
                          dest_media_agent,
                          src_media_agent,
                          config_only=False):
        """
        Moves a deduplication store

            Args:
                copy_name               (str)   -- name of the storage policy copy

                dest_path:              (str)   -- path where new partition is to be hosted

                src_path:               (str)   -- path where existing partition is hosted

                dest_media_agent:       (str)   -- media agent name where new partition is to be hosted

                src_media_agent:        (str)   -- media agent name where existing partition is hosted

                config_only             (bool)  -- to only chnage in DB (files need to be moved manually) (True/False)
                Default : False

            Returns:
                object - object - instance of the Job class for this DDB move job

            Raises:
                SDKException:
                    if type of input parameters is not string

                    if job failed

                    if response is empty

                    if response is not success
        """
        if not (isinstance(copy_name, str) and
                isinstance(dest_path, str) and
                isinstance(src_path, str) and
                isinstance(dest_media_agent, str) and
                isinstance(src_media_agent, str)):
            raise SDKException('Storage', '101')

        request = {
            "taskInfo": {
                "associations": [
                    {
                        "copyName": copy_name, "storagePolicyName": self.storage_policy_name
                    }
                ], "task": {
                    "taskType": 1,
                    "initiatedFrom": 1,
                    "policyType": 0,
                    "taskId": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                }, "subTasks": [
                    {
                        "subTaskOperation": 1, "subTask": {
                            "subTaskType": 1, "operationType": 5013
                        }, "options": {
                            "adminOpts": {
                                "libraryOption": {
                                    "operation": 20, "ddbMoveOption": {
                                        "flags": 2, "subStoreList": [
                                            {
                                                    "srcPath": src_path,
                                                    "changeOnlyDB": config_only,
                                                    "destPath": dest_path,
                                                    "destMediaAgent": {
                                                        "name": dest_media_agent
                                                    }, "srcMediaAgent": {
                                                        "name": src_media_agent
                                                    }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
        ddb_move = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', ddb_move, request
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'DDB move job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                else:
                    raise SDKException('Storage', '108')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add_ddb_partition(self,
                          copy_id,
                          sidb_store_id,
                          sidb_new_path,
                          media_agent):
        """
        Adds a new DDB partition
            Args:
                copy_id         (str)   -- storage policy copy id

                sidb_store_id   (str)   -- deduplication store id

                sidb_new_path   (str)   -- path where new partition is to be hosted

                media_agent     (str)   -- media agent on which new partition is to be hosted

            Raises:
                SDKException:
                    if type of input parameters is not string
        """
        if not (isinstance(copy_id, str) and
                isinstance(sidb_store_id, str) and
                isinstance(sidb_new_path, str) and
                isinstance(media_agent, str)):
            raise SDKException('Storage', '101')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, str):
            media_agent = MediaAgent(self._commcell_object, media_agent)

        request_xml = """
        <EVGui_ParallelDedupConfigReq commCellId="2" copyId="{0}" operation="15">
        <SIDBStore SIDBStoreId="{1}"/>
        <dedupconfigItem commCellId="0">
        <maInfoList><clientInfo id="{2}" name="{3}"/>
        <subStoreList><accessPath path="{4}"/>
        </subStoreList></maInfoList></dedupconfigItem>
        </EVGui_ParallelDedupConfigReq>

        """.format(copy_id, sidb_store_id, media_agent.media_agent_id,
                   media_agent.media_agent_name, sidb_new_path)
        self._commcell_object._qoperation_execute(request_xml)

    def get_copy(self, copy_name):
        """Returns a storage policy copy object if copy exists

            Args:
               copy_name (str)  --  name of the storage policy copy

            Returns:
               object - instance of the StoragePolicyCopy class for the given copy name

            Raises:
               SDKException:
                   if type of the copy name argument is not string

                   if no copy exists with the given name
        """
        if not isinstance(copy_name, str):
            raise SDKException('Storage', '101')

        if self.has_copy(copy_name):
            return StoragePolicyCopy(self._commcell_object, self.storage_policy_name, copy_name)
        else:
            raise SDKException(
                'Storage', '102', 'No copy exists with name: {0}'.format(copy_name)
            )

    def get_primary_copy(self):
        """Returns the primary copy of the storage policy

            Returns:
                object  -   Instance of the StoragePolicyCopy class of the primary copy

            Raises:
               SDKException:
                   if unable to find a primary copy in the storage policy

        """

        for copy_name, copy_info in self.copies.items():
            if copy_info['isDefault']:
                return self.get_copy(copy_name)

        raise SDKException('Storage', '102', 'Unable to find a primary copy in the storage policy')

    def get_secondary_copies(self):
        """Returns all the secondary copies in the storage policy sorted by copy precedence

            Returns:
                list    -   A list of storage policy copy instances.

        """

        sorted_copies = sorted(self.copies.items(), key=lambda x: x[1]['copyPrecedence'])  # Sort by copy precedence
        result = []

        for copy_name, copy_info in sorted_copies:
            if not copy_info['isDefault'] and not copy_info['isSnapCopy']:  # Skip primary copy and snap primary copies
                copy_obj = self.get_copy(copy_name)
                result.append(copy_obj)

        return result

    def mark_for_recovery(self, store_id, sub_store_id, media_agent_name, dedupe_path):
        """ Marks Deduplication store for recovery

            Args:
               store_id         (str)  --  SIDB store id

               sub_store_id     (str)  --  SIDB substore id

               media_agent_name (str)  --  name of the media agent on which DDB is hosted

               dedupe_path      (str)  --  SIDB store path
        """

        request_xml = """
                <EVGui_IdxSIDBSubStoreOpReq><info SIDBStoreId="{0}" SubStoreId="{1}" opType="1" path="{3}">
                <mediaAgent name="{2}"/>
                </info>
                </EVGui_IdxSIDBSubStoreOpReq>
                """.format(store_id, sub_store_id, media_agent_name, dedupe_path)
        self._commcell_object._qoperation_execute(request_xml)

    def run_recon(self, copy_name, sp_name, store_id, full_reconstruction=0, use_scalable_resource='false'):
        """ Runs non-mem DB Reconstruction job

            Args:
               copy_name    (str)  --  name of the storage policy copy

               sp_name      (str)  --  name of the storage policy

               store_id     (str)  --  SIDB store id associated with the copy

               full_reconstruction      (int)  --  flag to enable full reconstruction job
                                                   Valid values:
                                                   0: to start regular reconstruction job
                                                   1: to start full reconstruction job

               use_scalable_resource    (str)  --  to enable scalable resources
                                                   Valid values:
                                                   'true': to start old way reconstruction job
                                                   'false': to start reconstruction job with scalable resources
        """
        request_xml = """
        <TMMsg_DedupSyncTaskReq flags="0">
            <taskInfo><associations _type_="0" appName="" applicationId="0" backupsetId="0" backupsetName=""
            clientId="0" clientName="" clientSidePackage="1" commCellId="0" consumeLicense="1" copyName="{0}"
            instanceId="1" instanceName="" srmReportSet="0" srmReportType="0" storagePolicyName="{1}"
            subclientId="0" subclientName="" type="0"/>
            <subTasks>
                <options>
                    <adminOpts>
                        <contentIndexingOption subClientBasedAnalytics="0"/>
                        <dedupDBSyncOption SIDBStoreId="{2}"/>
                        <reconstructDedupDBOption allowMaximum="0" flags="{4}" noOfStreams="0" useScallableResourceManagement="{3}">
                        <mediaAgent _type_="11" mediaAgentId="0" mediaAgentName="&lt;ANY MEDIAAGENT>"/>
                        </reconstructDedupDBOption>
                    </adminOpts>
                    <restoreOptions>
                        <virtualServerRstOption isBlockLevelReplication="0"/>
                    </restoreOptions>
                </options>
                <subTask operationType="4036" subTaskType="1"/>
            </subTasks>
            <task initiatedFrom="1" ownerId="1" ownerName="admin" policyType="0" sequenceNumber="0"
            taskId="0" taskType="1"><taskFlags disabled="0"/>
            </task>
            </taskInfo>
        </TMMsg_DedupSyncTaskReq>
        """.format(copy_name, sp_name, store_id, use_scalable_resource, full_reconstruction)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json():
                return response.json()

    def reassociate_all_subclients(self, dest_storage_policy_name='CV_DEFAULT'):
        """
        Reassociates all subclients associated to Storage Policy
        Args:
            dest_storage_policy_name(str):  Name of a Storage Policy to which the Subclients are to
                                            be reassociated.
                                            Default Value:
                                            'CV_DEFAULT': 'Not Assigned' to any Policy.
        Raises:
            SDKException    :   If failed to reassociate
        """
        request_json = {
            "App_ReassociateStoragePolicyReq": {
                "forceNextBkpToFull": True,
                "newStoragePolicy": {
                    "storagePolicyName": dest_storage_policy_name
                },
                "currentStoragePolicy": {
                    "storagePolicyName": self.storage_policy_name
                }
            }
        }
        reassociate_subclients = self._commcell_object._services['EXECUTE_QCOMMAND']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', reassociate_subclients, request_json
        )
        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json()['errorCode'])
                    if error_code != 0:
                        error_message = "Failed to Reassociate the Subclients"
                        raise SDKException('Storage', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def start_over(self):
        """
        performs a start over operation on the specified storage policy/gdsp

            Args:

            Raises:
                  SDKException -- if response is bad/ flag is false

        returns None
        """
        dependent_flag = self.storage_policy_properties["copy"][0]["dedupeFlags"].get("useGlobalDedupStore", 0)
        if dependent_flag == 1:
            raise Exception("Dependent policy cannot be started over ...")

        request = {
            "MediaManager_MMStartOverReq": {
                    "bSealDDB": True,
                    "storagePolicy": {
                        "storagePolicyName": self.storage_policy_name
                    }
                }
            }

        startover = self._commcell_object._services['EXECUTE_QCOMMAND']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', startover, request
        )

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json()['errorCode'])
                    if error_code != 0:
                        error_message = "Failed to Start Over"
                        raise SDKException('Storage', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def run_data_forecast(self, **kwargs):
        """runs data forecast and retention report generation operation

            Args:

                **kwargs    --  dict of keyword arguments as follows:

                    localeName      str     localeName for report [defaults to "en-us"]

            Raises:
                  SDKException -- if response is bad/ flag is false

            Returns None
                """
        request = {
                    "processinginstructioninfo": {},
                    "taskInfo": {
                        "task": {
                            "taskType": 1,
                            "initiatedFrom": 2,
                            "taskFlags": {
                                "disabled": False
                            }
                        },
                        "appGroup": {},
                        "subTasks": [
                            {
                                "subTaskOperation": 1,
                                "subTask": {
                                    "subTaskName": "",
                                    "subTaskType": 1,
                                    "operationType": 4004
                                },
                                "options": {
                                    "adminOpts": {
                                        "reportOption": {
                                            "showHiddenStoragePolicies": False,
                                            "showGlobalStoragePolicies": False,
                                            "storagePolicyCopyList": [
                                                {
                                                    "storagePolicyName": self.storage_policy_name
                                                }
                                            ],
                                            "mediaInfoReport": {
                                                "mediaLocIn": True,
                                                "mediaLocOut": True
                                            },
                                            "commonOpt": {
                                                "dateFormat": "mm/dd/yyyy",
                                                "overrideDateTimeFormat": 0,
                                                "reportType": 7738,
                                                "summaryOnly": False,
                                                "reportCustomName": "",
                                                "timeFormat": "hh:mm:ss am/pm",
                                                "onCS": True,
                                                "locale": {
                                                    "country": "English",
                                                    "language": "UnitedStates",
                                                    "localeName": kwargs.get("localeName", "en-us")
                                                },
                                                "outputFormat": {
                                                    "outputType": 1,
                                                    "isNetworkDrive": False
                                                }
                                            },
                                            "computerSelectionList": {
                                                "includeAll": True
                                            },
                                            "jobSummaryReport": {
                                                "subclientFilter": False
                                            },
                                            "dataRetentionForecastReport": {
                                                "pruneData": True,
                                                "retainedBeyondBasicRet": False,
                                                "forecastDays": 0,
                                                "unPrunableData": True,
                                                "sortByOption": 2
                                            },
                                            "agentList": [
                                                {
                                                    "type": 0,
                                                    "flags": {
                                                        "include": True
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }

        forecast = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', forecast, request)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Failed to Run Data Forecast\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                else:
                    raise SDKException('Storage', '108')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

class StoragePolicyCopy(object):
    """Class for performing storage policy copy operations for a specific storage policy copy"""

    def __init__(self, commcell_object, storage_policy, copy_name, copy_id=None):
        """Initialise the Storage Policy Copy class instance.

            Args:
                commcell_object (object)        --  instance of the Commcell class
                storage_policy  (str/object)    -- storage policy to which copy is associated with
                copy_name       (str)           -- copy name
                copy_id         (str)           -- copy ID
                Default : None

            Returns:
                object - instance of the StoragePolicyCopy class

        """
        self._copy_name = copy_name.lower()
        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services

        if isinstance(storage_policy, StoragePolicy):
            self.storage_policy = storage_policy
        else:
            self.storage_policy = StoragePolicy(self._commcell_object, storage_policy)

        self.storage_policy_id = self.storage_policy.storage_policy_id
        self._storage_policy_name = self.storage_policy.storage_policy_name
        self.storage_policy._initialize_storage_policy_properties()

        if copy_id is not None:
            self.copy_id = str(copy_id)
        else:
            self.copy_id = str(self.get_copy_id())

        self._copy_properties = None
        self._STORAGE_POLICY_COPY = self._services['STORAGE_POLICY_COPY'] % (
            self.storage_policy_id, self.copy_id)
        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Storage Policy Copy class instance for Storage Policy/ Copy: "{0}/{1}"'
        return representation_string.format(self._storage_policy_name, self._copy_name)

    @property
    def all_copies(self):
        """Returns dict of  the storage policy copy associated with this storage policy

            dict - consists of stoarge policy copy properties
                    "copyType": copy_type,
                    "active": active,
                    "copyId": copy_id,
                    "libraryName": library_name,
                    "copyPrecedence": copy_precedence
        """
        return self.storage_policy._copies[self._copy_name]

    def get_copy_id(self):
        """Gets the storage policy id asscoiated with the storage policy"""
        return self.all_copies["copyId"]

    def get_copy_Precedence(self):
        """Gets the copyprecendence asscoiated with the storage policy copy"""
        return self.all_copies["copyPrecedence"]

    @property
    def is_active(self):
        """Gets whether the Storage Policy Copy is active or not"""
        return bool(self._copy_properties.get('active'))

    @is_active.setter
    def is_active(self, active):
        """Marks the Storage Policy Copy as active/inactive (True/False)
            Args:
                active    (bool):    mark the Storage Policy Copy as active/inactive (True/False)

            Raises:
                SDKException:
                    if failed to update the property

                    if the type of 'active' input is not correct
        """
        if not isinstance(active, bool):
            raise SDKException('Storage', '101')

        self._copy_properties['active'] = int(active)
        self._set_copy_properties()

    def refresh(self):
        """Refresh the properties of the StoragePolicy."""
        self._get_copy_properties()

    def _get_request_json(self):
        """ Gets all the storage policy copy properties .

           Returns:
                dict - all storage policy copy properties put inside a dict

        """
        self._copy_properties["StoragePolicyCopy"]["storagePolicyName"] = self._storage_policy_name
        copy_json = {
            "storagePolicyCopyInfo": self._copy_properties
        }
        return copy_json

    def _get_copy_properties(self):
        """Gets the storage policy copy properties.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        flag, response = self._cvpysdk_object.make_request('GET', self._STORAGE_POLICY_COPY)
        if flag:
            if response.json() and 'copy' in response.json():
                self._copy_properties = response.json()['copy']

                self._storage_policy_flags = self._copy_properties.get('StoragePolicyFlags')

                self._copy_flags = self._copy_properties.get('copyFlags')

                self._extended_flags = self._copy_properties.get('extendedFlags')

                self._data_path_config = self._copy_properties.get('dataPathConfiguration')

                self._media_properties = self._copy_properties.get('mediaProperties')

                self._retention_rules = self._copy_properties.get('retentionRules')

                self._data_encryption = self._copy_properties.get('dataEncryption')

                self._dedupe_flags = self._copy_properties.get('dedupeFlags')

                self._media_agent = self._copy_properties.get('mediaAgent')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _set_copy_properties(self):
        """sets the properties of this storage policy copy.

            Raises:
                SDKException:
                    if failed to update number properties for subclient

        """
        request_json = self._get_request_json()
        flag, response = self._cvpysdk_object.make_request('PUT', self._STORAGE_POLICY_COPY,
                                                           request_json)
        self.refresh()
        if flag:
            if response.json():
                if "response" in response.json():
                    error_code = str(
                        response.json()["response"][0]["errorCode"])

                    if error_code == "0":
                        return True, "0", ""
                    else:
                        error_message = ""

                        if "errorString" in response.json()["response"][0]:
                            error_message = response.json(
                            )["response"][0]["errorString"]

                        if error_message:
                            return (False, error_code, error_message)
                        else:
                            return (False, error_code, "")
            else:
                raise SDKException('Response', '111')
        else:
            raise SDKException('Response', '101')

    @property
    def copy_name(self):
        """Returns the name of the copy"""
        return self._copy_name

    @property
    def override_pool_retention(self):
        """Returns if Override Pool Retention flag is set or not"""
        return bool(self._extended_flags.get('overRideGACPRetention', 0))

    @override_pool_retention.setter
    def override_pool_retention(self, override):
        """Sets/Unsets the override Pool Retention Flag. Not Applicable for Storage Pool Copies

        Args:
            override(bool)  :   Override the pool Retention (True/False)
        """
        self._extended_flags['overRideGACPRetention'] = int(override)
        self._set_copy_properties()

    @property
    def copy_retention(self):
        """Treats the copy retention as a read-only attribute."""
        retention_values = {}
        retention_values["days"] = self._retention_rules['retainBackupDataForDays']
        retention_values["cycles"] = self._retention_rules['retainBackupDataForCycles']
        retention_values["archiveDays"] = self._retention_rules['retainArchiverDataForDays']
        retention_values["jobs"] = self._retention_rules['jobs']
        return retention_values

    @copy_retention.setter
    def copy_retention(self, retention_values):
        """Sets the copy retention as the value provided as input.
            Args:
                retention_values    (tuple) --  retention values to be set on a copy

                    tuple:

                        **int** -   value to specify retainBackupDataForDays

                        **int** -   value to specify retainBackupDataForCycles

                        **int** -   value to specify retainArchiverDataForDays

                        **int** -   value to specify jobs

                    e.g. :
                         storage_policy_copy.copy_retention = (30, 15, 1, 8)

            Raises:
                SDKException:
                    if failed to update retention values on the copy

        """
        if retention_values[0] >= 0:
            self._retention_rules['retainBackupDataForDays'] = retention_values[0]
        if retention_values[1] >= 0:
            self._retention_rules['retainBackupDataForCycles'] = retention_values[1]
        if retention_values[2] >= 0:
            self._retention_rules['retainArchiverDataForDays'] = retention_values[2]
        if len(retention_values) > 3:
            self._retention_rules['jobs'] = retention_values[3]
            if retention_values[3] > 0:
                self._retention_rules['retentionFlags']['jobBasedRetention'] = 1
            else:
                self._retention_rules['retentionFlags']['jobBasedRetention'] = 0

        self._set_copy_properties()

    @property
    def copy_software_compression(self):
        """Treats the copy software compression setting as a read-only attribute."""
        return 'compressionOnClients' in self._extended_flags

    def set_copy_software_compression(self, value):
        """Sets the copy software compression setting as the value provided as input.
            Args:
                value    (bool) --  software compression value to be set on a copy (True/False)

            Raises:
                SDKException:
                    if failed to update compression values on copy

                    if the type of value input is not correct

        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')

        if value is False:
            if 'compressionOnClients' in self._extended_flags:
                self._extended_flags['compressionOnClients'] = 0

        self._extended_flags['compressionOnClients'] = int(value)
        self._set_copy_properties()

    @property
    def copy_dedupe_dash_full(self):
        """Treats the copy deduplication setting as a read-only attribute."""
        return 'enableDASHFull' in self._dedupe_flags

    @copy_dedupe_dash_full.setter
    def copy_dedupe_dash_full(self, value):
        """Sets the copy deduplication setting as the value provided as input.
            Args:
                value    (bool) --  dash full value to be set on a copy (True/False)

            Raises:
                SDKException:
                    if failed to update deduplication values on copy

                    if the type of value input is not correct

        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')

        if value is False:
            if 'enableSourceSideDiskCache' in self._dedupe_flags:
                self._dedupe_flags['enableSourceSideDiskCache'] = 0

        self._dedupe_flags['enableDASHFull'] = int(value)
        self._set_copy_properties()

    @property
    def copy_dedupe_disk_cache(self):
        """Treats the copy deduplication setting as a read-only attribute."""
        return 'enableSourceSideDiskCache' in self._dedupe_flags

    @copy_dedupe_disk_cache.setter
    def copy_dedupe_disk_cache(self, value):
        """Sets the copy deduplication setting as the value provided as input.
            Args:
                value    (bool) --  disk cache value to be set on a copy (True/False)

            Raises:
                SDKException:
                    if failed to update deduplication values on copy

                    if the type of value input is not correct
        """

        if not isinstance(value, bool):
            raise SDKException('Storage', '101')
        self._dedupe_flags['enableSourceSideDiskCache'] = int(value)

        self._set_copy_properties()

    @property
    def store_priming(self):
        """Treats the copy store priming setting as a read-only attribute."""
        return self._dedupe_flags.get('useDDBPrimingOption', 0) > 0

    @store_priming.setter
    def store_priming(self, value):
        """Sets the copy store priming setting as the value provided as input.
            Args:
                value    (bool) --  store priming flag to be set on a copy (True/False)

            Raises:
                SDKException:
                    if failed to update deduplication values on copy

                    if the type of value input is not correct

        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')

        self._dedupe_flags['useDDBPrimingOption'] = int(value)

        self._set_copy_properties()

    @property
    def copy_client_side_dedup(self):
        """Treats the copy deduplication setting as a read-only attribute."""
        return 'enableClientSideDedup' in self._dedupe_flags

    @copy_client_side_dedup.setter
    def copy_client_side_dedup(self, value):
        """Sets the copy deduplication setting as the value provided as input.
            Args:
                value    (bool) --  client side dedupe value to be set on a copy (True/False)

            Raises:
                SDKException:
                    if failed to update deduplication values on copy

                    if the type of value input is not correct

        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')

        self._dedupe_flags['enableClientSideDedup'] = int(value)

        self._set_copy_properties()

    def is_dedupe_enabled(self):
        """
        checks whether deduplication is enabled on the give storage policy copy
        returns Boolean
        """
        return bool(self._dedupe_flags.get('enableDeduplication', 0))

    @property
    def source_copy(self):
        """Treats the copy deduplication setting as a read-only attribute."""
        return self._copy_properties.get('sourceCopy', {}).get('copyName')

    @source_copy.setter
    def source_copy(self, copy_name):
        """Sets the source copy as provided in the input.

                    Args:
                    copy_name            (str)       name of the source copy

                    Raises:
                        SDKException:
                            if failed to update source on copy

                            if the type of input is not correct

        **************************************************************************************
        eg :-
                tertiary_copy.source_copy = "secondary_copy"

        """
        policy = self._commcell_object.storage_policies.get(self._storage_policy_name)
        copy = policy.get_copy(copy_name)

        if not isinstance(copy_name, str):
            raise SDKException('Storage', '101')

        if not self._copy_properties.get('sourceCopy', False):
            self._copy_properties['sourceCopy'] = {}

        self._copy_properties['sourceCopy']['copyId'] = copy.get_copy_id()
        self._copy_properties['sourceCopy']['copyName'] = copy.copy_name

        self._set_copy_properties()

    def set_encryption_properties(self, **props):
        """sets copy encryption properties based on given inputs

            Args:

                **props         dict of keyword arguments as follows:

                    preserve            (Bool)      whether to set preserve source encryption or not    default:False

                    plain_text          (Bool)      whether to store as plaintext or not                default:False

                    network_encryption       (Bool)      whether to set network encryption or not       default:False

                    re_encryption          (Bool)      whether to set re-encryption or not              default:False

                    encryption_type            (str)       encryption type specification             default:"BlowFish"

                    encryption_length          (int)       encryption key length specification          default:128

            Returns:
                  SDKException:
                            if failed to set copy encryption
                            if the type of inputs are not correct

            ***********************************************************************************************************

            to preserve encryption --> set_encryption_properties(preserve=True)

            to store as plaintext --> set_encryption_properties(plaintext=True)

            to set network encryption --> set_encryption_properties(plaintext=True, network_encryption=True,
                                                                    encryption_type="BlowFish", encryption_length=128)

            to set re-encryption --> set_encryption_properties(re_encryption=True,
                                                               encryption_type="BlowFish", encryption_length=128)

            ***********************************************************************************************************

            <Encryption_type>   <Encryption_length>

            "Blowfish"                  128
            "Blowfish"                  256
            "TwoFish"                   128
            "TwoFish"                   256
            "Serpent"                   128
            "Serpent"                   256
            "GOST"                      256
            "AES"                       128
            "AES"                       256
            "DES3"                      192
        """
        preserve = props.get('preserve', False)
        plain_text = props.get('plain_text', False)
        network_encryption = props.get('network_encryption', False)
        re_encryption = props.get('re_encryption', False)
        encryption_type = props.get('encryption_type', 'BlowFish')
        encryption_length = props.get('encryption_length', 128)

        if not isinstance(preserve, bool) or \
                not isinstance(plain_text, bool) or \
                not isinstance(network_encryption, bool) or \
                not isinstance(re_encryption, bool) or \
                not isinstance(encryption_type, str) or \
                not isinstance(encryption_length, int):
            raise SDKException('Storage', '101')

        self._copy_flags['preserveEncryptionModeAsInSource'] = int(preserve)
        self._copy_flags['auxCopyReencryptData'] = int(re_encryption)
        self._copy_flags['storePlainText'] = int(plain_text)
        self._copy_flags['encryptOnNetworkUsingSelectedCipher'] = int(network_encryption)

        self._copy_properties['extendedFlags']['encryptOnDependentPrimary'] = 0

        if plain_text and not network_encryption:

            self._copy_properties['dataEncryption'] = {}

        else:

            if "dataEncryption" not in self._copy_properties:
                self._copy_properties["dataEncryption"] = {
                    "encryptData": 0
                }
                self._data_encryption = self._copy_properties["dataEncryption"]

        if re_encryption or network_encryption:

            self._data_encryption['encryptData'] = 1
            self._data_encryption['encryptionType'] = encryption_type
            self._data_encryption['encryptionKeyLength'] = encryption_length

            if re_encryption:
                self._copy_properties['extendedFlags']['encryptOnDependentPrimary'] = 1

        self._set_copy_properties()

    @property
    def copy_reencryption(self):
        """Treats the secondary copy encryption as a read-only attribute."""
        if 'auxCopyReencryptData' in self._copy_flags:
            if self._copy_flags['auxCopyReencryptData'] == 1:
                encryption_setting = "True"

        if 'preserveEncryptionModeAsInSource' in self._copy_flags:
            if self._copy_flags['preserveEncryptionModeAsInSource'] == 1:
                encryption_setting = "False"

        return encryption_setting

    @copy_reencryption.setter
    def copy_reencryption(self, encryption_values):
        """Sets the secondary copy encryption as the value provided as input.
            Args:
                encryption_values    (tuple) --  encryption values to be set on a copy

                    tuple:

                        **bool** -   value to specify encrypt data [True/False]

                        **str** -   value to specify cipher type

                        **int** -   value to specify key length [128/256]

                        **int** -   value to specify GDSP dependent copy [True/False]

                    e.g. :
                        to enable encryption:
                            storage_policy_copy.copy_reencryption = (True, "TWOFISH", "128", False)

                        to disable encryption:
                            storage_policy_copy.copy_reencryption = (False, "",0, False)

            Raises:
                SDKException:
                    if failed to update encryption settings for copy

                    if the type of value input is not correct
        """
        if "dataEncryption" not in self._copy_properties:
            self._copy_properties["dataEncryption"] = {
                "encryptData": "",
                "encryptionType": "",
                "encryptionKeyLength": ""}
            self._data_encryption = self._copy_properties["dataEncryption"]

        if not isinstance(encryption_values[0], bool):
            raise SDKException('Storage', '101')

        if int(encryption_values[0]) == 0:
            if int(encryption_values[3]) == 1:
                self._copy_properties['extendedFlags']['encryptOnDependentPrimary'] = 0
            self._copy_properties["dataEncryption"] = {
                "encryptData": 0
            }
            self._copy_flags['auxCopyReencryptData'] = 0
            self._copy_flags['preserveEncryptionModeAsInSource'] = 1

        if int(encryption_values[0]) == 1:
            if (isinstance(encryption_values[1], str)
                    and isinstance(encryption_values[2], int)):
                self._copy_properties['extendedFlags']['encryptOnDependentPrimary'] = 1
                self._copy_flags['auxCopyReencryptData'] = 1
                self._copy_flags['preserveEncryptionModeAsInSource'] = 0
                self._data_encryption['encryptData'] = 1
                self._data_encryption['encryptionType'] = encryption_values[1]
                self._data_encryption['encryptionKeyLength'] = encryption_values[2]
            else:
                raise SDKException('Response', '110')

        self._set_copy_properties()

    @property
    def copy_precedence(self):
        """Gets the copy precedence of the copy"""
        return self.all_copies["copyPrecedence"]

    @property
    def media_agent(self):
        """Gets the media agent name of the copy"""
        return self._media_agent.get('mediaAgentName')

    def get_jobs_on_copy(self, from_date=None, to_date=None, backup_type=None, retained_by=0,
                         include_to_be_copied_jobs=False, list_partial_jobs_only=False):
        """Fetches the Details of jobs on Storage Policy Copy

        Args:
            from_date      (str): Start Date Range for the Jobs
                                    [format-'yyyy/mm/dd'] [default: from start]

            to_date        (str): End Date Range for the Jobs
                                    [format-'yyyy/mm/dd'] [default: till date]

            backup_type    (str): Filter by backup type [default: None(all backup types)]
                                    Valid values: 'full'/'incr'

            retained_by    (int): Filter by retention type of jobs [default: 0]
                                    Valid values:
                                    1: basic retention
                                    2: extended retention
                                    4: manual retention

            include_to_be_copied_jobs   (bool): Include details on jobs that are in to be copied state [default: False]

            list_partial_jobs_only      (bool): Get details of jobs that are in partially copied state only
                                                  [default: False]

        Returns:
            (list)  :   List of dict's with each dict containing details of a job
        Raises:
            SDKException:   if the response/fetch operation failed
        """
        command = f"qoperation execscript -sn QS_JobsinSPCopy -si @i_policyName='{self._storage_policy_name}'" \
                  f" -si @i_copyName='{self.copy_name}'"
        if from_date:
            command = f"{command} -si @i_fromTime='{from_date}'"
        if to_date:
            command = f"{command} -si @i_toTime='{to_date}'"
        if backup_type:
            command = f"{command} -si @i_backupType='{backup_type.lower()}'"
        if retained_by:
            command = f"{command} -si @i_retention='{retained_by}'"
        if include_to_be_copied_jobs:
            command = f"{command} -si @i_includeToBeCopiedJobs='1'"
        if list_partial_jobs_only:
            command = f"{command} -si @i_includePartialJobsOnly='1'"

        response = self._commcell_object.execute_qcommand(command)
        if response.json():
            json_response = response.json()
            if json_response.get("ExecScriptOutput"):
                if isinstance(json_response.get("ExecScriptOutput").get("FieldValue"), list):
                    return json_response.get("ExecScriptOutput").get("FieldValue")
                if isinstance(json_response.get("ExecScriptOutput").get("FieldValue"), dict):
                    if json_response.get("ExecScriptOutput").get("FieldValue").get("@JobID"):
                        return [json_response.get("ExecScriptOutput").get("FieldValue")]
                return []
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '102', response_string)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def delete_job(self, job_id):
        """
        Deletes a job on Storage Policy
            Args:
                job_id      (str)   --  ID for the job to be deleted

        Raises:
            SDKException:
                if type of input parameters is not string
        """
        if not isinstance(job_id, str):
            raise SDKException('Storage', '101')

        request_xml = """
        <App_JobOperationCopyReq operationType="2">
        <jobList appType="" commCellId="2" jobId="{0}"><copyInfo copyName="{1}" storagePolicyName="{2}"/></jobList>
        <commCellInfo commCellId="2"/></App_JobOperationCopyReq>
        """.format(job_id, self._copy_name, self._storage_policy_name)

        self._commcell_object._qoperation_execute(request_xml)

    def _mark_jobs_on_copy(self, job_id, operation):
        """Marks job(s) for given operation on a secondary copy

        Args:
            job_id      (int or str or list): Job Id(s) that needs to be marked
            operation   (str):  Operation that the job(s) needs to be marked for.
                                Operations Supported: (allowcopy/recopy/donotcopy/
                                markJobsBad/pickForVerification/donotPickForVerification)
        Raises:
            SDKException:
                if type of input parameters is not string or List of strings
        """
        if not isinstance(job_id, str) and not isinstance(job_id, int):
            if not isinstance(job_id, list) or\
                    (not all(isinstance(id, int) for id in job_id) and not all(isinstance(id, str) for id in job_id)):
                raise SDKException('Storage', '101')

        # send multiple requests to counter limit of URL length in IIS
        job_strings = []
        if isinstance(job_id, list):
            string = ''
            for id in job_id:
                string += f',{id}'
                if len(string) > 200:
                    job_strings.append(string.strip(','))
                    string = ''
            if string:
                job_strings.append(string.strip(','))
        else:
            job_strings.append(job_id)

        for string in job_strings:
            qcommand = f' -sn MarkJobsOnCopy -si {self._storage_policy_name} -si {self._copy_name} -si {operation} -si {string}'
            url = self._services['EXECUTE_QSCRIPT'] % (qcommand)
            flag, response = self._commcell_object._cvpysdk_object.make_request("POST", url)
            if flag:
                if response.text:
                    if 'jobs do not belong' in response.text.lower():
                        raise SDKException('Storage', '102', response.text.strip())
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

    def pick_for_copy(self, job_id):
        """Marks job(s) to be Picked for Copy to a secondary copy

        Args:
            job_id      (int or str or list): Job Id(s) that needs to be marked
        """
        self._mark_jobs_on_copy(job_id, 'allowcopy')

    def recopy_jobs(self, job_id):
        """Marks job(s) to be picked for ReCopying to a secondary copy

        Args:
            job_id      (int or str or list): Job Id(s) that needs to be marked
        """
        self._mark_jobs_on_copy(job_id, 'recopy')

    def do_not_copy_jobs(self, job_id):
        """Marks job(s) as Do Not Copy to a secondary copy

        Args:
            job_id      (int or str or list):   Job Id(s) that needs to be marked
        """
        self._mark_jobs_on_copy(job_id, 'donotcopy')

    def pick_jobs_for_data_verification(self, job_id):
        """Marks job(s) on a copy to be Picked for Data Verification

        Args:
            job_id      (int or str or list):   Job Id(s) that needs to be marked
        """
        self._mark_jobs_on_copy(job_id, 'pickForVerification')

    def do_not_verify_data(self, job_id):
        """Marks job(s) on a copy to not be Picked for Data Verification

        Args:
            job_id      (int or str or list):   Job Id(s) that needs to be marked
        """
        self._mark_jobs_on_copy(job_id, 'donotPickForVerification')

    def mark_jobs_bad(self, job_id):
        """Marks job(s) on a copy as Bad

        Args:
            job_id      (int or str or list):   Job Id(s) that needs to be marked
        """
        self._mark_jobs_on_copy(job_id, 'markJobsBad')

    @property
    def extended_retention_rules(self):
        """Treats the extended retention rules setting as a read-only attribute."""

        mapping = {
            2: "EXTENDED_ALLFULL",
            4: "EXTENDED_WEEK",
            8: "EXTENDED_MONTH",
            16: "EXTENDED_QUARTER",
            32: "EXTENDED_HALFYEAR",
            64: "EXTENDED_YEAR",
            128: "MANUALLY_PIN",
            256: "EXTENDED_GRACE_WEEK",
            512: "EXTENDED_GRACE_MONTH",
            1024: "EXTENDED_GRACE_QUARTER",
            2048: "EXTENDED_GRACE_HALFYEAR",
            4096: "EXTENDED_GRACE_YEAR",
            8192: "EXTENDED_CANDIDATE_WEEK",
            16384: "EXTENDED_CANDIDATE_MONTH",
            32768: "EXTENDED_CANDIDATE_QUARTER",
            65536: "EXTENDED_CANDIDATE_HALFYEAR",
            131072: "EXTENDED_CANDIDATE_YEAR",
            262144: "EXTENDED_HOUR",
            524288: "EXTENDED_DAY",
            1048576: "EXTENDED_CANDIDATE_HOUR",
            2097152: "EXTENDED_CANDIDATE_DAY",
            4194304: "EXTENDED_GRACE_HOUR",
            8388608: "EXTENDED_GRACE_DAY",
            16777216: "EXTENDED_LAST_JOB",
            33554432: "EXTENDED_FIRST",
        }
        rule_one = dict()
        rule_two = dict()
        rule_three = dict()
        if 'extendedRetentionRuleOne' in self._retention_rules:
            rule_one['isEnabled'] = self._retention_rules['extendedRetentionRuleOne']['isEnabled']
            rule_one['rule'] = mapping[self._retention_rules['extendedRetentionRuleOne']['rule']]
            rule_one['endDays'] = self._retention_rules['extendedRetentionRuleOne']['endDays']
            rule_one['graceDays'] = self._retention_rules['extendedRetentionRuleOne']['graceDays']
        else:
            rule_one = False

        if 'extendedRetentionRuleTwo' in self._retention_rules:
            rule_two['isEnabled'] = self._retention_rules['extendedRetentionRuleTwo']['isEnabled']
            rule_two['rule'] = mapping[self._retention_rules['extendedRetentionRuleTwo']['rule']]
            rule_two['endDays'] = self._retention_rules['extendedRetentionRuleTwo']['endDays']
            rule_two['graceDays'] = self._retention_rules['extendedRetentionRuleTwo']['graceDays']
        else:
            rule_two = False

        if 'extendedRetentionRuleThree' in self._retention_rules:
            rule_three['isEnabled'] = self._retention_rules['extendedRetentionRuleThree']['isEnabled']
            rule_three['rule'] = mapping[self._retention_rules['extendedRetentionRuleThree']['rule']]
            rule_three['endDays'] = self._retention_rules['extendedRetentionRuleThree']['endDays']
            rule_three['graceDays'] = self._retention_rules['extendedRetentionRuleThree']['graceDays']
        else:
            rule_three = False
        return rule_one, rule_two, rule_three

    @extended_retention_rules.setter
    def extended_retention_rules(self, extended_retention):
        """Sets the copy extended retention rules as the value provided as input

            Args:
                extended_retention   (tuple)     --  to set extended_retention rules

                    tuple:
                        **int**    -   which rule to set (1/2/3)

                        **bool**    -   value for isEnabled

                        **str**     -   value for rule

                        Example valid values:
                            EXTENDED_ALLFULL
                            EXTENDED_WEEK
                            EXTENDED_MONTH
                            EXTENDED_QUARTER
                            EXTENDED_HALFYEAR
                            EXTENDED_YEAR

                        **int**     -   value for endDays

                        **int**     -   value for graceDays

                    e.g.:

                        >>> copy_obj.extended_retention_rules = [1, True, "EXTENDED_ALLFULL", 0, 0]

            Raises:
                SDKException:
                    if failed to update extended Retention Rule on copy

        """
        mapping = {
            1: 'extendedRetentionRuleOne',
            2: 'extendedRetentionRuleTwo',
            3: 'extendedRetentionRuleThree'
        }

        rule = mapping[extended_retention[0]]
        if rule not in self._copy_properties:
            self._retention_rules[rule] = {
                "isEnabled": "",
                "rule": "",
                "endDays": "",
                "graceDays": ""}

        if extended_retention[0] is not None:
            self._retention_rules[rule]['isEnabled'] = int(extended_retention[1])
            self._retention_rules[rule]['rule'] = extended_retention[2]
            self._retention_rules[rule]['endDays'] = extended_retention[3]
            self._retention_rules[rule]['graceDays'] = extended_retention[4]
        else:
            raise SDKException('Storage', '110')

        self._set_copy_properties()

    @property
    def copy_retention_managed_disk_space(self):
        """Treats managed disk space setting as a read-only attribute"""
        return 'enableManagedDiskSpace' in self._retention_rules

    @copy_retention_managed_disk_space.setter
    def copy_retention_managed_disk_space(self, managed_disk_space_value):
        """Sets managed disk space attribute value with provided input value

            Args:
             managed_disk_space_value (Bool) -- managed disk space value to be enabled/disabled

            Raises:
                SDKException:

                    if the type of value input is not correct

        """
        if not isinstance(managed_disk_space_value, bool):
            raise SDKException('Storage', '101')

        if not managed_disk_space_value:
            self._retention_rules['retentionFlags']['enableManagedDiskSpace'] = 0
        if managed_disk_space_value:
            self._retention_rules['retentionFlags']['enableManagedDiskSpace'] = 1
        self._set_copy_properties()

    @property
    def is_parallel_copy(self):
        """Treats the parallel copy setting as a read-only attribute."""
        return 'enableParallelCopy' in self._copy_flags

    def set_parallel_copy(self, value):
        """ Sets the parallel copy on storage policy copy as the value provided as input.
            Args:
                value    (bool) --  parallel copy on storage policy copy value to be set on a copy (True/False)

            Raises:
                SDKException:
                    if failed to update parallel copy on storage policy copy

                    if the type of value input is not correct
        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')

        self._copy_flags['enableParallelCopy'] = int(value)

        self._set_copy_properties()

    @property
    def space_optimized_auxillary_copy(self):
        """Treats the space optimized auxillary copy setting as a read-only attribute."""
        if self._copy_properties.get('extendedFlags', {}).get('spaceOptimizedAuxCopy'):
            return True
        return False

    @space_optimized_auxillary_copy.setter
    def space_optimized_auxillary_copy(self, value):
        """Sets the space optimized auxillary copy setting as the value provided as input.
            Args:
                value    (bool) --  Enable/Disable Space Optimized Auxillary Copy
            Raises:
                SDKException:
                    if failed to update property

                    if the type of value input is not correct
        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')
        self._copy_properties['extendedFlags']['spaceOptimizedAuxCopy'] = int(value)

        self._set_copy_properties()

    @property
    def is_inline_copy(self):
        """Treats the inline copy setting as a read-only attribute."""
        return 'inlineAuxCopy' in self._copy_flags

    def set_inline_copy(self, value):
        """ Sets the inline copy on storage policy copy as the value provided as input.
            Args:
                value    (bool) --  inline copy on storage policy copy value to be set on a copy (True/False)

            Raises:
                SDKException:
                    if failed to update inline copy on storage policy copy

                    if the type of value input is not correct
        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')

        self._copy_flags['inlineAuxCopy'] = int(value)

        self._set_copy_properties()

    @property
    def network_throttle_bandwidth(self):
        """Treats the Network Throttle Bandwidth as a read-only attribute.

            Returns:
                (int) : Value of Network Throttle Bandwidth set in MBPH
        """
        return int(self._copy_properties.get('throttleNetworkBandWidthMBHR'))

    @network_throttle_bandwidth.setter
    def network_throttle_bandwidth(self, value):
        """ Sets the Network Throttle Bandwidth on storage policy copy as the value provided as input.
            Args:
                value    (int):  value of Network Throttle Bandwidth in MBPH

            Raises:
                SDKException:
                    if failed to update Network Throttle Bandwidth on storage policy copy

                    if the type of value input is not correct
        """
        if not isinstance(value, int):
            raise SDKException('Storage', '101')

        self._copy_properties['throttleNetworkBandWidthMBHR'] = value
        self._set_copy_properties()

    def add_svm_association(self, src_array_id, source_array, tgt_array_id,
                            target_array, **kwargs):
        """ Method to add SVM association on Replica/vault and Mirror Copy

            Agrs:
                src_array_id    (int)   --  Controlhost id of source SVM

                source_array    (str)   --  Name of the source Array

                tgt_array_id    (int)   --  Controlhost id of target SVM

                target_array    (str)   --  Name of the Target Array

                target_vendor   (str)   --  Target Vendor Name
                
                tgt_vendor_id   (int)   --  Target Vendor id

        """
        target_vendor = kwargs.get('target_vendor', "")
        tgt_vendor_id = kwargs.get('tgt_vendor_id', 0)

        request_json = {
            "EVGui_MMSMArrayReplicaPairReq": {
                "processinginstructioninfo": {
                    "locale": {
                        "_type_": 66,
                        "localeId": 0
                    },
                    "formatFlags": {
                        "ignoreUnknownTags": True,
                        "elementBased": False,
                        "skipIdToNameConversion": True,
                        "formatted": False,
                        "filterUnInitializedFields": False,
                        "skipNameToIdConversion": False,
                        "continueOnError": False
                    },
                    "user": {
                        "_type_": 13,
                        "userName": "admin",
                        "userId": 1
                    }
                },
                "copyId": self.copy_id,
                "flags": 0,
                "operation": 2,
                "userId": 1,
                "replPairList": [
                    {
                        "copyId": 0,
                        "flags": 0,
                        "replicaPairId": 0,
                        "srcArray": {
                            "name": source_array,
                            "id": src_array_id
                        },
                        "vendor": {
                            "name": "",
                            "id": 0
                        },
                        "tgtVendor": {
                            "name": target_vendor,
                            "id": tgt_vendor_id
                        },
                        "tgtArray": {
                            "name": target_array,
                            "id": tgt_array_id
                        }
                    }
                ]
            }
        }

        add_svm_association_service = self._commcell_object._services['EXECUTE_QCOMMAND']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_svm_association_service, request_json
        )
        self.refresh()

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json()['errorCode'])
                    if error_code != 0:
                        error_message = "Failed to Update SVM Association on Copy: {0}".format(
                            self._copy_name
                        )
                        raise SDKException('Storage', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def set_key_management_server(self, kms_name):
        """Sets the Key Management Server to this copy

            Args:
                kms_name  (str) -- The Key Management Server's name

            Raises SDKException:
                If input is not valid

                If API response is not successful

        """
        if not isinstance(kms_name, str):
            raise SDKException('Storage', '101')

        self._copy_properties["dataEncryption"] = {
            "keyProviderName": kms_name,
            "rotateMasterKey": True
        }
        self._set_copy_properties()
    
    def set_multiplexing_factor(self, mux_factor):
        """Sets/Unset the multiplexing factor for the storage policy copy

            Args:
                mux_factor  (int) -- The value for multiplexing factor

            Raises SDKException:
                If input is not valid

                If API response is not successful
        """
        if not isinstance(mux_factor, int):
            raise SDKException('Storage', '101')

        self._copy_properties['mediaProperties'] = {
            "multiplexingFactor" : mux_factor
        }
        self._set_copy_properties()
