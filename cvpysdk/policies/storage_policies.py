# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

    run_snapshot_cataloging()               --  Runs the deferred catalog job from Commcell

    run_aux_copy()                          --  starts a aux copy job for this storage policy and
    returns the job object

    refresh()                               --  refresh the properties of the storage policy

    update_transactional_ddb()              --  enable/disable transactional DDB option on a DDB

    seal_ddb()                              --  seal a DDB store

    add_ddb_partition()                     --  Adds a new DDB partition

    move_dedupe_store()                     --  Moves a deduplication store

    run_ddb_verification()                  --  Runs DDB verification job

    get_copy()                              --  Returns the StoragePolicyCopy class object of the input copy



StoragePolicyCopy:
    __init__(self, commcell_object,
                storage_policy_name,
                copy_name, copy_id)         --  initialize the instance of StoragePolicy class for
                                                a specific storage policy of the commcell

    __repr__()                              --  returns a string representation of the
                                                StoragePolicy instance

    get_copy_id()		                    --	Gets the storage policy id asscoiated with the storage policy

    refresh()		                        --	Refresh the properties of the StoragePolicy

    _get_request_json()	                    --	Gets all the storage policy copy properties

    _get_copy_properties()	                --	Gets the storage policy copy properties

    _set_copy_properties()	                --	sets the properties of this storage policy copy

    delete_job()                            --  delete a job from storage policy copy node

    recopy_jobs()                           --  recopies a job on a secondary copy

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode

from past.builtins import basestring
from future.standard_library import install_aliases

from ..exception import SDKException
from ..job import Job

from ..storage import DiskLibrary
from ..storage import MediaAgent

install_aliases()


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
        if not isinstance(policy_name, basestring):
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
        if not isinstance(storage_policy_name, basestring):
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

    def add(self,
            storage_policy_name,
            library,
            media_agent,
            dedup_path=None,
            incremental_sp=None,
            retention_period=5,
            number_of_streams=None,
            ocum_server=None):
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
                default: 5

                number_of_streams   (int)         --  the number of streams for the storage policy
                default: None

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
        from urllib.parse import urlencode

        if ((dedup_path is not None and not isinstance(dedup_path, basestring)) or
                (not (isinstance(storage_policy_name, basestring) and
                      isinstance(retention_period, int))) or
                (incremental_sp is not None and not isinstance(incremental_sp, basestring))):
            raise SDKException('Storage', '101')

        if isinstance(library, DiskLibrary):
            disk_library = library
        elif isinstance(library, basestring):
            disk_library = DiskLibrary(self._commcell_object, library)
        else:
            raise SDKException('Storage', '104')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, basestring):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        else:
            raise SDKException('Storage', '103')

        if dedup_path or incremental_sp:
            encode_dict = {
                "storagepolicy": storage_policy_name,
                "mediaagent": media_agent.media_agent_name,
                "library": disk_library.library_name
            }
            if dedup_path:
                encode_dict["deduppath"] = dedup_path
            if incremental_sp:
                encode_dict["incstoragepolicy"] = incremental_sp

            web_service = self._POLICY + '?' + urlencode(encode_dict)

            flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', web_service)

            if flag:
                try:
                    if response.json():
                        if 'errorCode' in response.json() and 'errorMessage' in response.json():
                            error_message = response.json()['errorMessage'].split('\n')[0]
                            o_str = 'Failed to add storage policy\nError: "{0}"'

                            raise SDKException('Storage', '102', o_str.format(error_message))

                except ValueError:
                    if response.text:
                        # initialize the policies again
                        # so the policies object has all the policies
                        self.refresh()
                        return response.text.strip()
                    else:
                        raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
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
                "storagePolicyName": storage_policy_name
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
                        "storagePolicyFlags": {
                            "enableSnapshot": 1
                            },
                        "retentionRules" : {
                            "retainBackupDataForCycles": 1
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
                    if 'archiveGroupCopy' in response.json():
                        # initialize the policies again
                        # so the policies object has all the policies
                        self.refresh()

                    elif 'error' in response.json():
                        error_message = response.json()['error']['errorMessage']
                        o_str = 'Failed to create storage policy\nError: "{0}"'

                        raise SDKException('Storage', '102', o_str.format(error_message))
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

            return self.get(storage_policy_name)

    def add_tape_sp(self, storage_policy_name, library, media_agent, drive_pool, scratch_pool):
        """
        Adds storage policy with tape data path
        Args:
                storage_policy_name (str)         --  name of the new storage policy to add

                library             (str)          --  name or instance of the library
                to add the policy to

                media_agent         (str/object)  --  name or instance of media agent
                to add the policy to

                drive_pool          (str)         --  Drive pool name of the tape library

                scratch_pool      (str)          --  Scratch pool name of the tape library

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

        from urllib.parse import urlencode
        if not (isinstance(drive_pool, basestring) and
                isinstance(scratch_pool, basestring) and
                isinstance(library, basestring) and
                isinstance(media_agent, basestring) and
                isinstance(storage_policy_name, basestring)):
            raise SDKException('Storage', '101')

        tape_library = library
        encode_dict = {"storagepolicy": storage_policy_name, "mediaagent": media_agent,
                       "library": tape_library, "drivepool": drive_pool,
                       "scratchpool": scratch_pool}
        web_service = self._POLICY + '?' + urlencode(encode_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', web_service)

        if flag:
            try:
                if response.json():
                    if 'errorCode' in response.json():
                        error_code = response.json()['errorCode']
                        if error_code != 0:
                            o_str = 'Failed to add storage policy\nError: "{0}"'
                            raise SDKException('Storage', '102', o_str.format(error_code))

            except ValueError:
                if response.text:
                    # initialize the policies again
                    # so the policies object has all the policies
                    self.refresh()
                    return response.text.strip()
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
        if not isinstance(storage_policy_name, basestring):
            raise SDKException('Storage', '101')

        if self.has_policy(storage_policy_name):
            policy_delete_service = self._POLICY + '/{0}'.format(storage_policy_name)

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', policy_delete_service
            )

            if flag:
                try:
                    if response.json():
                        if 'errorCode' in response.json() and 'errorMessage' in response.json():
                            error_message = response.json()['errorMessage']
                            o_str = 'Failed to delete storage policy\nError: "{0}"'

                            raise SDKException('Storage', '102', o_str.format(error_message))
                except ValueError:
                    if response.text:
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
        self._storage_policy_properties = None
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
                library_name = copy['library']['libraryName']
                copy_precedence = copy['copyPrecedence']
                is_snap = bool(int(copy['isSnapCopy']))
                temp = {
                    "copyType": copy_type,
                    "active": active,
                    "copyId": copy_id,
                    "libraryName": library_name,
                    "copyPrecedence": copy_precedence,
                    "isSnapCopy": is_snap
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
        if not isinstance(copy_name, basestring):
            raise SDKException('Storage', '101')

        return self._copies and copy_name.lower() in self._copies

    def create_secondary_copy(self,
                              copy_name,
                              library_name,
                              media_agent_name,
                              drive_pool=None,
                              spare_pool=None,
                              tape_library_id=None,
                              drive_pool_id=None,
                              spare_pool_id=None,
                              snap_copy=False):
        """Creates Synchronous copy for this storage policy

            Args:
                copy_name           (str)   --  copy name to create

                library_name        (str)   --  library name to be assigned

                media_agent_name    (str)   --  media_agent to be assigned

                snap_copy           (bool)  --  boolean on whether copy should be a snap copy
                default: False

            Raises:
                SDKException:
                    if type of inputs in not string

                    if copy with given name already exists

                    if failed to create copy

                    if response received is empty

                    if response is not success
        """
        if not (isinstance(copy_name, basestring) and
                isinstance(library_name, basestring) and
                isinstance(media_agent_name, basestring)):
            raise SDKException('Storage', '101')

        if self.has_copy(copy_name):
            err_msg = 'Storage Policy copy "{0}" already exists.'.format(copy_name)
            raise SDKException('Storage', '102', err_msg)

        media_agent_id = self._commcell_object.media_agents._media_agents[media_agent_name.lower()]['id']

        snap_copy = int(snap_copy == True)

        if drive_pool is not None:
            request_xml = """
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
            request_xml = """
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

    def create_snap_copy(self,
                         copy_name,
                         is_mirror_copy,
                         is_snap_copy,
                         library_name,
                         media_agent_name,
                         source_copy,
                         provisioning_policy=None,
                         resource_pool=None,
                         is_replica_copy=None):
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

            Raises:
                SDKException:
                    if type of inputs in not string

                    if copy with given name already exists

                    if failed to create copy

                    if response received is empty

                    if response is not success
        """
        if not (isinstance(copy_name, basestring) and
                isinstance(library_name, basestring) and
                isinstance(media_agent_name, basestring)):
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

        request_xml = """
                    <App_CreateStoragePolicyCopyReq copyName="{0}">
                        <storagePolicyCopyInfo active="1" isMirrorCopy="{1}" isSnapCopy="{2}" provisioningPolicyName="{3}">
                            <StoragePolicyCopy _type_="18" copyName="{0}" storagePolicyName="{4}" />
                            <extendedFlags arrayReplicaCopy="{5}" useOfflineArrayReplication="{6}" />
                            <library _type_="9" libraryName="{7}" />
                            <mediaAgent _type_="11" mediaAgentName="{8}" />
                            <spareMediaGroup _type_="67" libraryName="{7}" />
                            <retentionRules retainArchiverDataForDays="-1" retainBackupDataForCycles="1" retainBackupDataForDays="0" />
                            <sourceCopy _type_="18" copyName="{9}" storagePolicyName="{4}" />
                            <resourcePoolsList operation="1" resourcePoolName="{10}" />
                        </storagePolicyCopyInfo>
                    </App_CreateStoragePolicyCopyReq>
                    """.format(copy_name, is_mirror_copy, is_snap_copy, provisioning_policy,
                               self.storage_policy_name, arrayReplicaCopy, useOfflineReplication,
                               library_name, media_agent_name, source_copy, resource_pool)

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
        if not isinstance(copy_name, basestring):
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
            source_copy_for_snapshot_catalog_id = self._copies[options['source_copy_for_snapshot_catalog'].lower()]['copyId']
        else:
            source_copy_for_snapshot_catalog_id = 0

        update_snapshot_tab_service = self._commcell_object._services['EXECUTE_QCOMMAND']

        request_xml = """
                    <EVGui_SetSnapOpPropsReq deferredCatalogOperation="{0}" snapshotToTapeOperation="{1}">
                        <header localeId="0" userId="0" />
                        <snapshotToTapeProps archGroupId="{2}" calendarId="1" dayNumber="0" deferredDays="0" 
                            enable="{3}" flags="0" infoFlags="0" numOfReaders="0" numPeriod="1" 
                            sourceCopyId="{4}" startTime="0" type="0" />
                        <deferredCatalogProps archGroupId="{2}" calendarId="1" dayNumber="0" deferredDays="0" 
                            enable="{5}" flags="0" infoFlags="0" numOfReaders="0" numPeriod="1" 
                            sourceCopyId="{6}" startTime="0" type="0" />
                    </EVGui_SetSnapOpPropsReq>
        """.format(defferred_catalog_value, backup_copy_value, self.storage_policy_id,
                   int(enable_backup_copy), source_copy_for_snap_to_tape_id,
                   int(enable_snapshot_catalog), source_copy_for_snapshot_catalog_id)

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
                     all_copies=True, total_jobs_to_process=0):
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
            if not (isinstance(storage_policy_copy_name, basestring) and
                    isinstance(media_agent, basestring)):
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

    def seal_ddb(self, copy_name):
        """
        Seals the deduplication database

            Args:
                copy_name   (str)   --  name of the storage policy copy

            Raises:
                SDKException:
                    if type of input parameters is not string
        """
        if not isinstance(copy_name, basestring):
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
        if not (isinstance(copy_name, basestring) and isinstance(media_agent_name, basestring)):
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
        if not (isinstance(copy_name, basestring) and
                isinstance(library_name, basestring) and
                isinstance(path, basestring) and
                isinstance(ddb_media_agent, basestring) and
                isinstance(media_agent_name, basestring)):
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
                             ddb_ver_level):
        """
        Runs DDB verification job

            Args:
                copy_name       (str)   --  name of the copy which is associated with the DDB store

                ver_type        (str)   --  backup level (Full/Incremental)

                ddb_ver_level   (str)   --  DDB verification type
                                            (DDB_VERIFICATION/ DDB_AND_DATA_VERIFICATION /
                                            QUICK_DDB_VERIFICATION/ DDB_DEFRAGMENTATION)

            Returns:
                object - instance of the Job class for this DDB verification job

            Raises:
                SDKException:
                    if type of input parameters is not string

                    if job failed

                    if response is empty

                    if response is not success
        """
        if not (isinstance(copy_name, basestring) and
                isinstance(ver_type, basestring) and
                isinstance(ddb_ver_level, basestring)):
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
                                "subTaskType": 1, "operationType": 4007
                            },
                            "options": {
                                "backupOpts": {
                                    "mediaOpt": {
                                        "auxcopyJobOption": {
                                            "maxNumberOfStreams": 0,
                                            "allCopies": True,
                                            "useMaximumStreams": True,
                                            "useScallableResourceManagement": False,
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
                                        "backupLevel": ver_type
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
        if not (isinstance(copy_name, basestring) and
                isinstance(dest_path, basestring) and
                isinstance(src_path, basestring) and
                isinstance(dest_media_agent, basestring) and
                isinstance(src_media_agent, basestring)):
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
        if not (isinstance(copy_id, basestring) and
                isinstance(sidb_store_id, basestring) and
                isinstance(sidb_new_path, basestring) and
                isinstance(media_agent, basestring)):
            raise SDKException('Storage', '101')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, basestring):
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
        if not isinstance(copy_name, basestring):
            raise SDKException('Storage', '101')

        if self.has_copy(copy_name):
            return StoragePolicyCopy(self._commcell_object, self.storage_policy_name, copy_name)
        else:
            raise SDKException(
                'Storage', '102', 'No copy exists with name: {0}'.format(copy_name)
            )


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
    def copy_retention(self):
        """Treats the copy retention as a read-only attribute."""
        retention_values = {}
        retention_values["days"] = self._retention_rules['retainBackupDataForDays']
        retention_values["cycles"] = self._retention_rules['retainBackupDataForCycles']
        retention_values["archiveDays"] = self._retention_rules['retainArchiverDataForDays']
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

                    e.g. :
                         storage_policy_copy.copy_retention = (30, 15, 1)

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
                            storage_policy_copy.copy_encryption = (True, "TWOFISH", "128", False)

                        to disable encryption:
                            storage_policy_copy.copy_encryption = (False, "",0, False)

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
            if (isinstance(encryption_values[1], basestring)
                    and isinstance(encryption_values[2], int)):
                self._copy_flags['auxCopyReencryptData'] = 1
                self._copy_flags['preserveEncryptionModeAsInSource'] = 0
                self._data_encryption['encryptData'] = 1
                self._data_encryption['encryptionType'] = encryption_values[1]
                self._data_encryption['encryptionKeyLength'] = encryption_values[2]
            else:
                raise SDKException('Response', '110')

        self._set_copy_properties()

    def delete_job(self, job_id):
        """
        Deletes a job on Storage Policy
            Args:
                job_id      (str)   --  ID for the job to be deleted

        Raises:
            SDKException:
                if type of input parameters is not string
        """
        if not isinstance(job_id, basestring):
            raise SDKException('Storage', '101')

        request_xml = """
        <App_JobOperationCopyReq operationType="2">
        <jobList appType="" commCellId="2" jobId="{0}"><copyInfo copyName="{1}" storagePolicyName="{2}"/></jobList>
        <commCellInfo commCellId="2"/></App_JobOperationCopyReq>
        """.format(job_id, self._copy_name, self._storage_policy_name)

        self._commcell_object._qoperation_execute(request_xml)

    def recopy_jobs(self, job_id):
        """ recopies a job on a secondary copy

            Args:
                job_id      (str)   -- Job Id that needs to be deleted

            Raises:
                SDKException:
                    if type of input parameters is not string

        """
        if not isinstance(job_id, basestring):
            raise SDKException('Storage', '101')

        qcommand = """ -sn MarkJobsOnCopy -si {0} -si {1} -si recopy -si {2}""".format(
            self._storage_policy_name, self._copy_name, job_id)
        url = self._services['EXECUTE_QSCRIPT'] % (qcommand)
        flag, response = self._commcell_object._cvpysdk_object.make_request("POST", url)
        if flag:
            if response.ok is not True:
                raise SDKException('Response', '101',
                                   self._commcell_object._update_response_(response.text))
            else:
                return True

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

        if managed_disk_space_value == False:
            self._retention_rules['retentionFlags']['enableManagedDiskSpace'] = 0
        if managed_disk_space_value == True:
            self._retention_rules['retentionFlags']['enableManagedDiskSpace'] = 1
        self._set_copy_properties()

    def add_svm_association(self, src_array_id, source_array, tgt_array_id, target_array):
        """ Method to add SVM association on Replica/vault and Mirror Copy

            Agrs:
                src_array_id    (int)   --  Controlhost id of source SVM

                source_array    (str)   --  Name of the source Array

                tgt_array_id    (int)   --  Controlhost id of target SVM

                target_array    (str)   --  Name of the Target Array

        """

        request_json = {
            "EVGui_MMSMArrayReplicaPairReq":{
                "processinginstructioninfo":{
                    "locale":{
                        "_type_":66,
                        "localeId":0
                    },
                    "formatFlags":{
                        "ignoreUnknownTags":True,
                        "elementBased":False,
                        "skipIdToNameConversion":True,
                        "formatted":False,
                        "filterUnInitializedFields":False,
                        "skipNameToIdConversion":False,
                        "continueOnError":False
                    },
                    "user":{
                        "_type_":13,
                        "userName":"admin",
                        "userId":1
                    }
                },
                "copyId": self.copy_id,
                "flags":0,
                "operation":2,
                "userId":1,
                "replPairList":[
                    {
                        "copyId":0,
                        "flags":0,
                        "replicaPairId":0,
                        "srcArray":{
                            "name": source_array,
                            "id": src_array_id
                        },
                        "tgtArray":{
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
