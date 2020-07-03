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

"""Main file for performing storage related operations on the commcell.

This file has all the classes related to Storage operations.

MediaAgents:      Class for representing all the media agents attached to the commcell.

MediaAgent:       Class for representing a single media agent attached to the commcell.

DiskLibraries:    Class for representing all the disk libraries attached to the commcell.

DiskLibrary:      Class for representing a single disk library associated with the commcell.


MediaAgents:
    __init__(commcell_object)   --  initialize the MediaAgents class instance for the commcell

    __str__()                   --  returns all the media agents associated with the commcell

    __repr__()                  --  returns the string for the instance of the MediaAgents class

    _get_media_agents()         --  gets all the media agents of the commcell

    all_media_agents()          --  returns all the media agents on the commcell

    has_media_agent()           --  checks if a media agent exists with the given name or not

    get(media_agent_name)       --  returns the instance of MediaAgent class
    of the media agent specified
    
    delete(media_agent)     --  Deletes the media agent from the commcell.

    refresh()                   --  refresh the media agents associated with the commcell


MediaAgent:
    __init__(commcell_object,
             media_agent_name,
             media_agent_id)                --  initialize the instance of MediaAgent class for a
    specific media agent of the commcell

    __repr__()                              --  returns a string representation of the
    MediaAgent instance

    _get_media_agent_id()                   --  gets the id of the MediaAgent instance from
    commcell

    _get_media_agent_properties()           --  returns media agent properties

    _initialize_media_agent_properties()    --  initializes media agent properties

    enable_power_management()               --  Enable VM Management (power management)

    _perform_power_operation()              --  Performs power operation (power-on/power-off)

    power_on()                              --  Power-on MediaAgent if VM management is enabled

    power_off()                             --  Power-off MediaAgent if VM management is enabled

    wait_for_power_status()                 -- Waits till the expected power status is not achieved

    media_agent_name()                      --  returns media agent name

    media_agent_id()                        --  returns media agent id

    is_online()                             --  returns True is media agent is online

    platform()                              --  returns os info of the media agent

    refresh()                               --  refresh the properties of the media agent

    change_index_cache()                    --  runs catalog migration

    index_cache_path()                      --  returns index cache path of the media agent

    index_cache_enabled()                   --  returns index cache enabled status

    set_state()                    -- enables/disables media agent

    mark_for_maintenance() -- marks/unmarks media agent offline for maintenance

DiskLibraries:
    __init__(commcell_object)   --  initialize the DiskLibraries class instance for the commcell

    __str__()                   --  returns all the disk libraries associated with the commcell

    __repr__()                  --  returns the string for the instance of the DiskLibraries class

    _get_libraries()            --  gets all the disk libraries of the commcell

    all_disk_libraries()        --  returns the dict of all the disk libraries on commcell

    has_library(library_name)   --  checks if a disk library exists with the given name or not

    add()                       --  adds a new disk library to the commcell

    delete()                    --  Deletes a disk library from commcell

    get(library_name)           --  returns the instance of the DiskLibrary class
    for the library specified

    refresh()                   --  refresh the disk libraries associated with the commcell


DiskLibrary:
    __init__(commcell_object,
             library_name,
             library_id)        --  initialize the instance of DiskLibrary class for a specific
    disk library of the commcell

    __repr__()                  --  returns a string representation of the DiskLibrary instance

    _get_library_id()           --  gets the id of the DiskLibrary instance from commcell

    move_mountpath()            --  To perform move mountpath operation

    validate_mountpath()        --  To perform storage validation on mountpath

    add_cloud_mount_path()      --  Adds a mount path to the cloud library

    add_mount_path()            --  adds the mount path on the local/ remote machine

    set_mountpath_reserve_space()      --  to set reserve space on the mountpath

    change_device_access_type()  -- to change device access type

    verify_media()              --  To perform verify media operation on media

    set_mountpath_preferred_on_mediaagent() --  Sets select preferred mountPath according to mediaagent setting on the
                                                library

    _get_library_properties()   --  gets the disk library properties

    refresh()                   --  Refresh the properties of this disk library.

DiskLibrary instance Attributes

    **media_agents_associated**  --  returns the media agents associated with the disk library
    **library_properties**       --  Returns the dictionary consisting of the full properties of the library
    **free_space**               --  returns the free space on the library
    **mountpath_usage**          --  returns mountpath usage on library

"""
from __future__ import absolute_import
from __future__ import unicode_literals
import uuid, time

from base64 import b64encode

from past.builtins import basestring
from future.standard_library import install_aliases
from .exception import SDKException

install_aliases()


class MediaAgents(object):
    """Class for getting all the media agents associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the MediaAgents class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the MediaAgents class
        """
        self._commcell_object = commcell_object
        self._MEDIA_AGENTS = self._commcell_object._services['GET_MEDIA_AGENTS']
        self._media_agents = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all media agents of the commcell.

            Returns:
                str - string of all the media agents associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Media Agent')

        for index, media_agent in enumerate(self._media_agents):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, media_agent)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the MediaAgents class."""
        return "MediaAgents class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_media_agents(self):
        """Gets all the media agents associated to the commcell specified by commcell object.

            Returns:
                dict - consists of all media agents of the commcell
                    {
                         "media_agent1_name": {

                                 'id': media_agent1_id,

                                 'os_info': media_agent1_os,

                                 'is_online': media_agent1_status
                         },
                         "media_agent2_name": {

                                 'id': media_agent2_id,

                                 'os_info': media_agent2_os,

                                 'is_online': media_agent2_status
                         }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._MEDIA_AGENTS
        )

        if flag:
            if response.json() and 'mediaAgentList' in response.json():
                media_agents = response.json()['mediaAgentList']
                media_agents_dict = {}

                for media_agent in media_agents:
                    temp_name = media_agent['mediaAgent']['mediaAgentName'].lower()
                    temp_id = str(media_agent['mediaAgent']['mediaAgentId']).lower()
                    temp_os = media_agent['osInfo']['OsDisplayInfo']['OSName']
                    temp_status = bool(media_agent['status'])
                    media_agents_dict[temp_name] = {
                        'id': temp_id,
                        'os_info': temp_os,
                        'is_online': temp_status
                    }

                return media_agents_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_media_agents(self):
        """Returns dict of all the media agents on this commcell

            dict - consists of all media agents of the commcell
                    {
                         "media_agent1_name": {

                                 'id': media_agent1_id,

                                 'os_info': media_agent1_os,

                                 'is_online': media_agent1_status
                         },
                         "media_agent2_name": {

                                 'id': media_agent2_id,

                                 'os_info': media_agent2_os,

                                 'is_online': media_agent2_status
                         }
                    }
        """
        return self._media_agents

    def has_media_agent(self, media_agent_name):
        """Checks if a media agent exists in the commcell with the input media agent name.

            Args:
                media_agent_name (str)  --  name of the media agent

            Returns:
                bool - boolean output whether the media agent exists in the commcell or not

            Raises:
                SDKException:
                    if type of the media agent name argument is not string
        """
        if not isinstance(media_agent_name, basestring):
            raise SDKException('Storage', '101')

        return self._media_agents and media_agent_name.lower() in self._media_agents

    def get(self, media_agent_name):
        """Returns a MediaAgent object of the specified media agent name.

            Args:
                media_agent_name (str)  --  name of the media agent

            Returns:
                object - instance of the MediaAgent class for the given media agent name

            Raises:
                SDKException:
                    if type of the media agent name argument is not string

                    if no media agent exists with the given name
        """
        if not isinstance(media_agent_name, basestring):
            raise SDKException('Storage', '101')
        else:
            media_agent_name = media_agent_name.lower()

            if self.has_media_agent(media_agent_name):
                return MediaAgent(self._commcell_object,
                                  media_agent_name,
                                  self._media_agents[media_agent_name]['id'])

            raise SDKException(
                'Storage', '102', 'No media agent exists with name: {0}'.format(media_agent_name)
            )
    
    def delete(self, media_agent, force=False):
        """Deletes the media agent from the commcell.

            Args:
                media_agent (str)  --  name of the Mediaagent to remove from the commcell
                
                force       (bool)     --  True if you want to delete media agent forcefully.

            Raises:
                SDKException:
                    if type of the media agent name argument is not string

                    if failed to delete Media agent

                    if response is empty

                    if response is not success

                    if no media agent exists with the given name

        """
        if not isinstance(media_agent, basestring):
            raise SDKException('Storage', '101')
        else:
            media_agent = media_agent.lower()

            if self.has_media_agent(media_agent):
                mediagent_id = self.all_media_agents[media_agent]['id']
                mediagent_delete_service = self._commcell_object._services['MEDIA_AGENT'] % (mediagent_id)
                if force:
                    mediagent_delete_service += "?forceDelete=1"

                flag, response = self._commcell_object._cvpysdk_object.make_request('DELETE', mediagent_delete_service)

                error_code = 0
                if flag:
                    if 'errorCode' in response.json():
                        o_str = 'Failed to delete mediaagent' 
                        error_code = response.json()['errorCode'] 
                        if error_code == 0:
                            # initialize the mediaagents again
                            # so the mediaagents object has all the mediaagents
                            self.refresh()
                        else:                                
                            error_message = response.json()['errorMessage']
                            if error_message:
                                o_str += '\nError: "{0}"'.format(error_message)                        
                            raise SDKException('Storage', '102', o_str)
                    else:
                        raise SDKException('Response', '102')
                else:
                    raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
            else:
                raise SDKException(
                    'Storage', '102', 'No Mediaagent exists with name: {0}'.format(media_agent)
                )

    def refresh(self):
        """Refresh the media agents associated with the Commcell."""
        self._media_agents = self._get_media_agents()


class MediaAgent(object):
    """Class for a specific media agent."""

    def __init__(self, commcell_object, media_agent_name, media_agent_id=None):
        """Initialise the MediaAgent object.

            Args:
                commcell_object   (object)  --  instance of the Commcell class

                media_agent_name  (str)     --  name of the media agent

                media_agent_id    (str)     --  id of the media agent
                    default: None

            Returns:
                object - instance of the MediaAgent class
        """
        self._commcell_object = commcell_object
        self._media_agent_name = media_agent_name.lower()
        self._media_agent_info = None
        if media_agent_id:
            self._media_agent_id = str(media_agent_id)
        else:
            self._media_agent_id = self._get_media_agent_id()

        self._MEDIA_AGENT = self._commcell_object._services['MEDIA_AGENT'] % (
            self._media_agent_name
        )

        self._CLOUD_MEDIA_AGENT = self._commcell_object._services['CLOUD_MEDIA_AGENT'] % (
            self._media_agent_id
        )

        self._CREATE_TASK = self._commcell_object._services['CREATE_TASK']
        self._MEDIA_AGENTS = self._commcell_object._services['GET_MEDIA_AGENTS'] + "/{0}".format(
            self.media_agent_id
        )

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'MediaAgent class instance for MA: "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self.media_agent_name, self._commcell_object.commserv_name
        )

    def _get_media_agent_id(self):
        """Gets the media agent id associated with this media agent.

            Returns:
                str - id associated with this media agent
        """
        media_agents = MediaAgents(self._commcell_object)
        return media_agents.get(self.media_agent_name).media_agent_id

    def _get_media_agent_properties(self):
        """Returns the media agent properties of this media agent.

            Returns:
                dict - dictionary consisting of the properties of this client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._MEDIA_AGENTS
        )

        if flag:
            if response.json() and 'mediaAgentList' in response.json():
                self._media_agent_info = response.json()['mediaAgentList'][0]
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_media_agent_properties(self):
        """Initializes the properties for this Media Agent"""
        self._status = None
        self._platform = None
        self._index_cache_enabled = None
        self._index_cache = None
        self._is_power_mgmt_allowed = None
        self._is_power_mgmt_supported = None
        self._is_power_management_enabled = None
        self._power_management_controller_name = None
        self._power_status = None

        properties = self._get_media_agent_properties()

        if properties['mediaAgentList']:
            mediaagent_list = properties['mediaAgentList'][0]
        else:
            raise SDKException('Response', '102')

        status = mediaagent_list.get('status')
        if status == 1:
            self._is_online = True
        else:
            self._is_online = False

        if mediaagent_list['osInfo']['OsDisplayInfo']['OSName']:
            platform = mediaagent_list['osInfo']['OsDisplayInfo']['OSName']
            if 'windows' in platform.lower():
                self._platform = 'WINDOWS'
            elif 'unix' in platform.lower() or 'linux' in platform.lower():
                self._platform = 'UNIX'
            else:
                self._platform = platform

        if mediaagent_list['mediaAgentProps']['mediaAgentIdxCacheProps']['cacheEnabled']:
            self._index_cache_enabled = mediaagent_list['mediaAgentProps'][
                'mediaAgentIdxCacheProps']['cacheEnabled']

        if mediaagent_list['mediaAgentProps']['mediaAgentIdxCacheProps']['cachePath']['path']:
            self._index_cache = mediaagent_list['mediaAgentProps']['mediaAgentIdxCacheProps'
                                                                   ]['cachePath']['path']

        if mediaagent_list['powerManagementInfo']['isPowerMgmtSupported']:
            self._is_power_mgmt_supported = mediaagent_list['powerManagementInfo']['isPowerMgmtSupported']

        if self._is_power_mgmt_supported:

            if mediaagent_list['powerManagementInfo']['isPowerManagementEnabled']:
                self._is_power_management_enabled = mediaagent_list['powerManagementInfo']['isPowerManagementEnabled']

            if mediaagent_list['powerManagementInfo']['isPowerMgmtAllowed']:
                self._is_power_mgmt_allowed = mediaagent_list['powerManagementInfo']['isPowerMgmtAllowed']

            if mediaagent_list['powerManagementInfo']['powerStatus']:
                self._power_status = mediaagent_list['powerManagementInfo']['powerStatus']

            if mediaagent_list['powerManagementInfo']['selectedCloudController']['clientName']:
                self._power_management_controller_name = mediaagent_list['powerManagementInfo']['selectedCloudController']['clientName']

    def enable_power_management(self, pseudo_client_name):
        """
            Enables power management using the provided cloud controller (pseudo client)

                Args :
                        pseudo_client_name : VSA pseudo client to be used as cloud controller
                Raises:
                        SDKException:
                                    If response is not success
                                    
                                    If Power management is not supported
        """
        if self._is_power_mgmt_allowed:
            client_obj = self._commcell_object._clients.get(pseudo_client_name)
            pseudo_client_name_client_id = client_obj._get_client_id()

            """
            payLoad = '<EVGui_SetCloudVMManagementInfoReq hostId="' + self.media_agent_id + '" useMediaAgent="1"> <powerManagementInfo isPowerManagementEnabled="1" > <selectedCloudController clientId="' + PseudoClientName_client_id + '" clientName="' + \
                      PseudoClientName + '"/></powerManagementInfo></EVGui_SetCloudVMManagementInfoReq>'
            """
            payLoad = '<EVGui_SetCloudVMManagementInfoReq hostId="{0}" useMediaAgent="1"> <powerManagementInfo isPowerManagementEnabled="1" > <selectedCloudController clientId="{1}" clientName="{2}"/></powerManagementInfo></EVGui_SetCloudVMManagementInfoReq>'.format(
                self.media_agent_id, pseudo_client_name_client_id, pseudo_client_name)

            response = self._commcell_object._qoperation_execute(payLoad)

            if response['errorCode'] != 0:
                raise SDKException('Response', '102', str(response))
        else:
            raise SDKException('Storage', '102', "Power management is not supported")

    def _perform_power_operation(self, operation):
        """
            Performs power operation

                Args :
                        self : Object
                        operation : Operation to perform
                        
                Raises:
                        SDKException:
                                        If operation is not 1 or 0
                                            
                                        If ower management is NOT enabled or NOT supported on MediaAgent

                                        If API response is empty

                                        If API response is not success
        """
        if not operation in ("1", "0"):
            raise SDKException('Response', '102',
                               "Invalid power operation type")

        if self._is_power_management_enabled:
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'GET', self._CLOUD_MEDIA_AGENT + "/" + operation
            )
            if not flag:
                raise SDKException('Response', '102',
                                   str(response))
            if response.json()['errorCode'] != 0:
                raise SDKException('Response', '102', str(response))
        else:
            raise SDKException('Storage', '102',
                               'Power management is NOT enabled or NOT supported')

    def power_on(self, wait_till_online=True):
        """
            Power-on the MediaAgent

                Args :
                        self : Object
                        wait_till_online :
                                            True : Waits until the MediaAgent is online
                                            False : Just submits the power-on request
        """

        if self.current_power_status not in ["Starting", "Started", "Online"]:
            self._perform_power_operation("1")

        if wait_till_online == True and self.current_power_status != "Online":
            self.wait_for_power_status("Online")

    def power_off(self, wait_till_stopped=True):
        """
            Power-off MediaAgent

                Args :
                        self : Object
                        wait_till_stopped :
                                            True : Waits until the MediaAgent is stopped
                                            False : Just submits the power-off request
        """

        if self.current_power_status not in ["Stopping", "Stopped"]:
            self._perform_power_operation("0")

        if wait_till_stopped == True and self.current_power_status != "Stopped":
            self.wait_for_power_status("Stopped")

    def wait_for_power_status(self, expected_power_status, time_out_sec=600):
        """
            Waits until the expected power status not achieved

                Args :
                                        self : Object
                                        expected_power_status : The expected power status as following.
                                                                    Starting
                                                                    Started
                                                                    Online
                                                                    Stopping
                                                                    Stopped
                                        time_out_sec : Maximum time to wait for the expected power status

                                        Raises:
                                                SDKException:
                                                                If time_out_sec is not an integer and time_out_sec not None

                                                                If expected power status is not achieved within time_out_sec time
        """
        if time_out_sec != None:
            if not isinstance(time_out_sec, int):
                raise SDKException('Storage', '102',
                                   'Expected an integer value for [time_out_sec]')

        start_time = time.time()
        while self.current_power_status != expected_power_status:
            time.sleep(10)
            if time_out_sec != None:
                if time.time() - start_time > time_out_sec:
                    raise SDKException('Storage', '102',
                                       'The expected power status is not achieved within expected time')

    def change_index_cache(self, old_index_cache_path, new_index_cache_path):
        """
        Begins a catalog migration job via the CreateTask end point.

            Args :
                old_index_cache_path - source index cache path

                new_index_cache_path - destination index cache path

            Returns :
                Returns job object of catalog migration job

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        conf_guid = str(uuid.uuid4())

        xml_options_string = '''<Indexing_IdxDirectoryConfiguration configurationGuid="{0}"
        icdPath="{1}" maClientFocusName="{2}" maGuid="" oldIcdPath="{3}"
        opType="0" />''' .format(
            conf_guid, new_index_cache_path, self.media_agent_name, old_index_cache_path)

        request_json = {
            "taskInfo": {
                "taskOperation": 1,
                "task": {
                    "isEZOperation": False,
                    "description": "",
                    "ownerId": 1,
                    "runUserId": 1,
                    "taskType": 1,
                    "ownerName": "",
                    "alertName": "",
                    "sequenceNumber": 0,
                    "isEditing": False,
                    "GUID": "",
                    "isFromCommNetBrowserRootNode": False,
                    "initiatedFrom": 3,
                    "policyType": 0,
                    "associatedObjects": 0,
                    "taskName": "",
                    "taskFlags": {
                        "notRunnable": False,
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskOrder": 0,
                            "subTaskType": 1,
                            "flags": 0,
                            "operationType": 5018,
                            "subTaskId": 1
                        },
                        "options": {
                            "originalJobId": 0,
                            "adminOpts": {
                                "catalogMigrationOptions": {
                                    "xmlOptions": xml_options_string,
                                    "mediaAgent": {
                                        "mediaAgentId": int(self._media_agent_id),
                                        "_type_": 11
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_TASK, request_json
        )

        if flag:
            if response.json() and 'jobIds' in response.json() and response.json()['jobIds'][0]:

                response_json = response.json()
                catalogmigration_jobid = response_json["jobIds"][0]
                catalogmigration_job_obj = self._commcell_object.job_controller.get(
                    catalogmigration_jobid)
                return catalogmigration_job_obj

            else:
                raise SDKException('Response', '102')

        else:
            raise SDKException('Response', '101')

    def set_state(self, enable=True):
        """
        disable the media agent by change in media agent properties.
            Args:
            enable      -   (bool)
                            True        - Enable the media agent
                            False       - Disable the media agent

            Raises:
            "exception"                  -   if there is an empty response
                                         -   if there is an error in request execution
                                         -   if response status is failure

        """

        if type(enable) != bool:
            raise SDKException('Storage', '101')

        media_id = int(self.media_agent_id)
        request_json = {
            "mediaAgentInfo": {
                "mediaAgent": {
                    "mediaAgentId": media_id
                },
                "mediaAgentProps": {
                    "enableMA": enable
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._MEDIA_AGENTS, request_json
        )

        # check for response
        # possible key errors if key not present in response, defaults set
        if flag:
            if response and response.json():
                response = response.json()
                if response.get('error', {}).get('errorCode', -1) != 0:
                    error_message = response.get('error', {}).get('errorString', '')
                    raise SDKException('Storage', '102', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')


    def mark_for_maintenance(self, mark=False):
        """
        mark the media agent offline for maintenance
            Args:
                mark  - (bool)
                                        True    - mark the media agent for maintenance
                                        False   - UNMARK the media agent for maintenance

            Raises:
            "exception"                  -   if there is an empty response
                                         -   if there is an error in request execution
                                         -   if response status is failure

        """

        if type(mark) != bool:
            raise SDKException('Storage', '101')

        media_id = int(self.media_agent_id)
        request_json = {
            "mediaAgentInfo": {
                "mediaAgent": {
                    "mediaAgentId": media_id
                },
                "mediaAgentProps": {
                    "markMAOfflineForMaintenance": mark
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._MEDIA_AGENTS, request_json
        )

        if flag:
            if response and response.json():
                response = response.json()
                if response.get('error', {}).get('errorCode', -1) != 0:
                    error_message = response.get('error', {}).get('errorString', '')
                    raise SDKException('Storage', '102', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')



    @property
    def name(self):
        """Returns the media agent display name"""
        return self._media_agent_info['mediaAgent']['displayName']

    @property
    def media_agent_name(self):
        """Treats the media agent name as a read-only attribute."""
        return self._media_agent_name

    @property
    def media_agent_id(self):
        """Treats the media agent id as a read-only attribute."""
        return self._media_agent_id

    @property
    def is_online(self):
        """Treats the status as read-only attribute"""
        return self._is_online

    @property
    def platform(self):
        """Treats the platform as read-only attribute"""
        return self._platform

    @property
    def index_cache_path(self):
        """Treats the index cache path as a read-only attribute"""
        return self._index_cache

    @property
    def index_cache_enabled(self):
        """Treats the cache enabled value as a read-only attribute"""
        return self._index_cache_enabled

    @property
    def current_power_status(self):
        """
                Returns the power state of the MA.

                    Args :
                            self : Object
                    Returns :
                            str - Current power status of the MediaAgent as following
                                    Starting : Power-on process in going on
                                    Started : MA is powered-on successfully but still not synced with CS
                                    Online : Powered-on and synced with CS. MA is ready to use.
                                    Stopping : Power-off operation is going on.
                                    Stopped : MA is powered-off
                                    Unknown : MA power status is still not synced with cloud provider. MA discovery is going on or power state sync with happening with cloud provider or something is NOT right.
        """
        self.refresh()
        power_status = {0: 'Unknown', 1: 'Starting', 2: 'Started', 3: 'Online', 4: 'Stopping', 5: 'Stopped'}
        return power_status.get(self._power_status)

    def refresh(self):
        """Refresh the properties of the MediaAgent."""
        self._initialize_media_agent_properties()


class DiskLibraries(object):
    """Class for getting all the disk libraries associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the DiskLibraries class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the DiskLibraries class
        """
        self._commcell_object = commcell_object
        self._LIBRARY = self._commcell_object._services['LIBRARY']

        self._libraries = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all disk libraries of the commcell.

            Returns:
                str - string of all the disk libraries associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Disk Library')

        for index, library in enumerate(self._libraries):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, library)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the DiskLibraries class."""
        return "DiskLibraries class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_libraries(self):
        """Gets all the disk libraries associated to the commcell specified by commcell object.

            Returns:
                dict - consists of all disk libraries of the commcell
                    {
                         "disk_library1_name": disk_library1_id,
                         "disk_library2_name": disk_library2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._LIBRARY)

        if flag:
            if response.json() and 'response' in response.json():
                libraries = response.json()['response']
                libraries_dict = {}

                for library in libraries:
                    temp_name = library['entityInfo']['name'].lower()
                    temp_id = str(library['entityInfo']['id']).lower()
                    libraries_dict[temp_name] = temp_id

                return libraries_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_disk_libraries(self):
        """Returns dict of all the disk libraries on this commcell

            dict - consists of all disk libraries of the commcell
                    {
                         "disk_library1_name": disk_library1_id,
                         "disk_library2_name": disk_library2_id
                    }

        """
        return self._libraries

    def has_library(self, library_name):
        """Checks if a library exists in the commcell with the input library name.

            Args:
                library_name (str)  --  name of the library

            Returns:
                bool - boolean output whether the library exists in the commcell or not

            Raises:
                SDKException:
                    if type of the library name argument is not string
        """
        if not isinstance(library_name, basestring):
            raise SDKException('Storage', '101')

        return self._libraries and library_name.lower() in self._libraries

    def add(self, library_name, media_agent, mount_path, username="", password="", servertype=0,
            saved_credential_name=""):
        """Adds a new Disk Library to the Commcell.

            Args:
                library_name (str)        --  name of the new library to add

                media_agent  (str/object) --  name or instance of media agent to add the library to

                mount_path   (str)        --  full path of the folder to mount the library at

                username     (str)        --  username to access the mount path
                    default: ""

                password     (str)        --  password to access the mount path
                    default: ""

                servertype   (int)        -- provide cloud library server type
                    default 0, value 59 for HPstore

                saved_credential_name   (str)   --  name of the saved credential
                    default: ""

            Returns:
                object - instance of the DiskLibrary class, if created successfully

            Raises:
                SDKException:
                    if type of the library name argument is not string

                    if type of the mount path argument is not string

                    if type of the username argument is not string

                    if type of the password argument is not string

                    if type of the media agent argument is not either string or MediaAgent instance

                    if failed to create disk library

                    if response is empty

                    if response is not success
        """
        if not (isinstance(library_name, basestring) and
                isinstance(mount_path, basestring) and
                isinstance(username, basestring) and
                isinstance(password, basestring)):
            raise SDKException('Storage', '101')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, basestring):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        else:
            raise SDKException('Storage', '103')

        request_json = {
            "isConfigRequired": 1,
            "library": {
                "mediaAgentId": int(media_agent.media_agent_id),
                "libraryName": library_name,
                "mountPath": mount_path,
                "loginName": username,
                "password": b64encode(password.encode()).decode(),
                "opType": 1,
                "savedCredential":{
                    "credentialName": saved_credential_name
                }
            }
        }

        if servertype > 0:
            request_json["library"]["serverType"] = servertype
            request_json["library"]["isCloud"] = 1

            if saved_credential_name:
                request_json["library"]["password"] = b64encode("XXXXX".encode()).decode()

            if servertype == 59:
                request_json["library"]["HybridCloudOption"] = {
                    "enableHybridCloud": "2", "diskLibrary": {"_type_": "9"}}
                request_json["library"]["savedCredential"] = {"_type_": "9"}

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._LIBRARY, request_json
        )

        if flag:
            if response.json():
                if 'library' in response.json():
                    library = response.json()['library']

                    # initialize the libraries again
                    # so the libraries object has all the libraries
                    self.refresh()

                    return DiskLibrary(
                        self._commcell_object,
                        library['libraryName'],
                        library_details=library)
                elif 'errorCode' in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to create disk library\nError: "{0}"'.format(error_message)

                    raise SDKException('Storage', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def delete(self, library_name):
        """deletes the specified library.

            Args:
                library_name (str)  --  name of the disk library to delete

            Raises:
                SDKException:
                    if type of the library name argument is not string
                    if no library exists with the given name
                    if response is incorrect
        """
        if not isinstance(library_name, basestring):
            raise SDKException('Storage', '101')

        if not self.has_library(library_name):
            raise SDKException('Storage',
                               '102',
                               'No library exists with name: {0}'.
                               format(library_name))

        request_json = {
            "EVGui_ConfigureStorageLibraryReq":
                {
                    "isDeconfigLibrary": 1,
                    "library":
                        {
                            "opType": 2,
                            "libraryName": library_name
                        }
                }
        }
        exec_command = self._commcell_object._services['EXECUTE_QCOMMAND']
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', exec_command, request_json)

        if flag:
            if response.json():
                if 'library' in response.json():
                    _response = response.json()['library']

                    if 'errorCode' in _response:
                        if _response['errorCode'] == 0:
                            self.refresh()
                        else:
                            raise SDKException('Storage', '102', _response['errorMessage'])
                else:
                    if 'errorMessage' in response.json():
                        o_str = 'Error: ' + response.json()['errorMessage']
                        raise SDKException('Response', '102', o_str)

                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            _stdout = 'Failed to delete library {0} with error: \n [{1}]'
            _stderr = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', _stdout.format(library_name, _stderr))

    def get(self, library_name):
        """Returns a DiskLibrary object of the specified disk library name.

            Args:
                library_name (str)  --  name of the disk library

            Returns:
                object - instance of the DiskLibrary class for the given library name

            Raises:
                SDKException:
                    if type of the library name argument is not string

                    if no disk library exists with the given name
        """
        if not isinstance(library_name, basestring):
            raise SDKException('Storage', '101')
        else:
            library_name = library_name.lower()

            if self.has_library(library_name):
                return DiskLibrary(self._commcell_object,
                                   library_name,
                                   self._libraries[library_name])

            raise SDKException(
                'Storage', '102', 'No disk library exists with name: {0}'.format(library_name)
            )

    def refresh(self):
        """Refresh the disk libraries associated with the Commcell."""
        self._libraries = self._get_libraries()


class DiskLibrary(object):
    """Class for a specific disk library."""

    def __init__(self, commcell_object, library_name, library_id=None, library_details=None):
        """Initialise the DiskLibrary object.

            Args:
                commcell_object  (object)  --  instance of the Commcell class

                library_name     (str)     --  name of the disk library

                library_id       (str)     --  id of the disk library
                    default: None

            Returns:
                object - instance of the DiskLibrary class
        """
        self._commcell_object = commcell_object
        self._library_name = library_name.lower()

        if library_id:
            self._library_id = str(library_id)
        else:
            self._library_id = self._get_library_id()
        self._library_properties_service = self._commcell_object._services[
            'GET_LIBRARY_PROPERTIES'] % (self._library_id)
        self._library_properties = self._get_library_properties()
        if library_details is not None:
            self.mountpath = library_details.get('mountPath', None)
            self.mediaagent = library_details.get('mediaAgentName', None)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'DiskLibrary class instance for library: "{0}" of Commcell: "{1}"'
        return representation_string.format(
            self.library_name, self._commcell_object.commserv_name
        )

    def move_mountpath(self, mountpath_id, source_device_path,
                       source_mediaagent_id, target_device_path, target_mediaagent_id):

        """ To perform move mountpath operation
        Args:
            mountpath_id  (int)   --  Mountpath Id that need to be moved.

            source_device_path (str)   -- Present Mountpath location

            source_mediaagent_id    (int)   -- MediaAgent Id on which present mountpath exists

            target_device_path    (str)   -- New Mountpath location

            target_mediaagent_id    (int)   -- MediaAgent Id on which new mountpath exists

        Returns:
            instance of the Job class for this move mountpath job

        Raises
            Exception:
                - if argument datatype is invalid

                - if API response error code is not 0

                - if response is empty

                - if response code is not as expected
        """

        if not (isinstance(mountpath_id, int) and
                isinstance(source_mediaagent_id, int) and
                isinstance(target_mediaagent_id, int) and
                isinstance(target_device_path, basestring) and
                isinstance(source_device_path, basestring)):
            raise SDKException('Storage', '101')

        request_xml = """<TMMsg_CreateTaskReq>
                        <taskInfo>
                            <task initiatedFrom="1" ownerId="1" sequenceNumber="0" taskId="0" taskType="1">
                                <taskFlags disabled="0" />
                            </task>
                            <associations mountPathId="{1}" />
                            <subTasks subTaskOperation="1">
                                <subTask operationType="5017" subTaskType="1" />
                                <options> <adminOpts> <libraryOption>
                                    <library libraryId="{0}" />
                                    <moveMPOption>
                                        <mountPathMoveList mountPathId="{1}" sourceDevicePath="{2}" 
                                        sourcemediaAgentId="{3}" targetDevicePath="{4}" targetMediaAgentId="{5}">
                                        <credential credentialId="0" credentialName=" " />
                                        </mountPathMoveList>
                                    </moveMPOption>
                                </libraryOption> </adminOpts> </options>
                            </subTasks>
                        </taskInfo>
                    </TMMsg_CreateTaskReq>""".format(self.library_id, mountpath_id, source_device_path,
                                                     source_mediaagent_id, target_device_path, target_mediaagent_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CREATE_TASK'], request_xml)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    from cvpysdk.job import Job
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                if "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Error: "{0}"'.format(error_message)
                    raise SDKException('Commcell', '105', o_str)

                else:
                    raise SDKException('Commcell', '105')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def validate_mountpath(self, mountpath_drive_id, media_agent):

        """ To perform storage validation on mountpath
        Args:
            mountpath_drive_id  (int)   --  Drive Id of mountpath that need to be validate.

            media_agent (str)   -- MediaAgent on which Mountpath exists

        Returns:
            instance of the Job class for this storage validation job

        Raises
            Exception:
                - if argument datatype is invalid

                - if API response error code is not 0

                - if response is empty

                - if response code is not as expected
        """

        if not (isinstance(mountpath_drive_id, int) and
                isinstance(media_agent, basestring)):
            raise SDKException('Storage', '101')


        request_xml = """<TMMsg_CreateTaskReq>
                        <taskInfo taskOperation="1">
                            <task associatedObjects="0" description="Storage Validation - Automation" initiatedFrom="1" 
                            isEZOperation="0" isEditing="0" isFromCommNetBrowserRootNode="0" ownerId="1" ownerName="" 
                            policyType="0" runUserId="1" sequenceNumber="0" taskType="1">
                            <taskFlags notRunnable="0" />
                            </task>
                            <subTasks subTaskOperation="1">
                                <subTask flags="0" operationType="4013" subTaskId="1" subTaskOrder="0" subTaskType="1"/>
                                <options originalJobId="0">
                                    <adminOpts>
                                        <libraryOption  operation="13" validationFlags="0" validattionReservedFlags="0">
                                            <library libraryId="{0}" />
                                            <mediaAgent mediaAgentName="{1}" />
                                            <driveIds driveId="{2}" />
                                            <validateDrive chunkSize="16384" chunksTillEnd="0" fileMarkerToStart="2"
                                             numberOfChunks="2" threadCount="2" volumeBlockSize="64" />
                                        </libraryOption> </adminOpts> </options> </subTasks>  </taskInfo>
                            </TMMsg_CreateTaskReq>""".format(self.library_id, media_agent, mountpath_drive_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CREATE_TASK'], request_xml
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    from cvpysdk.job import Job
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                if "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Error: "{0}"'.format(error_message)
                    raise SDKException('Commcell', '105', o_str)

                else:
                    raise SDKException('Commcell', '105')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def add_cloud_mount_path(self, mount_path, media_agent, username, password, server_type):
        """ Adds a mount path to the cloud library

        Args:
            mount_path  (str)   -- cloud container or bucket.

            media_agent (str)   -- MediaAgent on which mountpath exists

            username    (str)   -- Username to access the mount path in the format <Service Host>//<Account Name>
            Eg: s3.us-west-1.amazonaws.com//MyAccessKeyID. For more information refer http://documentation.commvault.com/commvault/v11/article?p=97863.htm.

            password    (str)   -- Password to access the mount path

            server_type  (int)   -- provide cloud library server type
                                    Eg: 3-Microsoft Azure Storage . For more information refer http://documentation.commvault.com/commvault/v11/article?p=97863.htm.
        Returns:
            None

        Raises
            Exception:
                - if mountpath or mediaagent or username or password or servertype arguments dataype is invalid

                - if servertype input data is incorrect

                - if API response error code is not 0

                - if response is empty

                - if response code is not as expected
            """

        if not (isinstance(mount_path, basestring) or isinstance(media_agent, basestring)
                or isinstance(username, basestring) or isinstance(password, basestring)
                or isinstance(server_type, int)):
            raise SDKException('Storage', '101')

        request_json = {
            "isConfigRequired": 1,
            "library": {
                "opType": 4,
                "isCloud": 1,
                "mediaAgentName": media_agent,
                "libraryName": self._library_name,
                "mountPath": mount_path,
                "loginName": username,
                "password": b64encode(password.encode()).decode(),
                "serverType": server_type
            }
        }

        exec_command = self._commcell_object._services['LIBRARY']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', exec_command, request_json
        )

        if flag:
            if response.json():
                if 'library' in response.json():
                    _response = response.json()['library']

                    if 'errorCode' in _response:
                        if _response['errorCode'] != 0:
                            raise SDKException('Storage', '102', _response['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            _stdout = 'Failed to add mount path [{0}] for library [{1}] with error: \n [{2}]'
            _stderr = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', _stdout.format(mount_path,
                                                                 self._library_name,
                                                                 _stderr))

    def _get_library_properties(self):
        """Gets the disk library properties.

            Returns:
                dict - dictionary consisting of the properties of this library

            Raises:
                SDKException:
                    if response is empty

                    if failed to get disk library properties

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._library_properties_service
        )

        if flag:
            if response.json():
                if 'libraryInfo' in response.json():
                    return response.json()['libraryInfo']
                raise SDKException('Storage', '102', 'Failed to get disk Library properties')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _get_library_id(self):
        """Gets the library id associated with this disk library.

            Returns:
                str - id associated with this disk library
        """
        libraries = DiskLibraries(self._commcell_object)
        return libraries.get(self.library_name).library_id

    def refresh(self):
        """Refresh the properties of this disk library."""
        self._library_properties = self._get_library_properties()

    def add_mount_path(self, mount_path, media_agent, username='', password=''):
        """ Adds a mount path [local/remote] to the disk library

        Args:
            mount_path  (str)   -- Mount path which needs to be added to disklibrary.
                                  This could be a local or remote mount path on mediaagent

            media_agent (str)   -- MediaAgent on which mountpath exists

            username    (str)   -- Username to access the mount path

            password    (str)   -- Password to access the mount path

        Returns:
            None

        Raises
            Exception:
                - if mountpath and mediaagent datatype is invalid

                - if API response error code is not 0

                - if response is empty

                - if response code is not as expected
            """

        if not isinstance(mount_path, basestring) or not isinstance(media_agent, basestring):
            raise SDKException('Storage', '101')

        request_json = {
            "EVGui_ConfigureStorageLibraryReq":
                {
                    "isConfigRequired": 1,
                    "library": {
                        "opType": 4,
                        "mediaAgentName": media_agent,
                        "libraryName": self._library_name,
                        "mountPath": mount_path,
                        "loginName": username,
                        "password": b64encode(password.encode()).decode(),
                    }
                }
        }

        exec_command = self._commcell_object._services['EXECUTE_QCOMMAND']

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            exec_command,
                                                                            request_json)
        if flag:
            if response.json():
                if 'library' in response.json():
                    _response = response.json()['library']

                    if 'errorCode' in _response:
                        if _response['errorCode'] != 0:
                            raise SDKException('Storage', '102', _response['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            _stdout = 'Failed to add mount path [{0}] for library [{1}] with error: \n [{2}]'
            _stderr = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', _stdout.format(mount_path,
                                                                 self._library_name,
                                                                 _stderr))

    def set_mountpath_reserve_space(self, mount_path, size):
        """
            To set reserve space on the mountpath
            Args:
                mount_path (str)    --  Mountpath

                size (int)          --  reserve space to be set in MB
        """

        request_json = {
            "EVGui_ConfigureStorageLibraryReq":
                {
                    "isConfigRequired": 1,
                    "library": {
                        "opType": 8,
                        "mediaAgentName": self.media_agent,
                        "libraryName": self._library_name,
                        "mountPath": mount_path
                    },
                    "libNewProp":{
                      "reserveSpaceInMB": size
                    }
                }
        }
        self._commcell_object.qoperation_execute(request_json)

    def change_device_access_type(self, mountpath_id, device_id, device_controller_id, media_agent_id,
                                  device_access_type):
        """
        To change device access type
            Args:
                mountpath_id (int)  -- Mount Path Id

                device_id (int)     -- Device Id

                device_controller_id (int) -- Device Controller Id

                media_agent_id (int)    --   Media Agent Id

                device_access_type (int)    --  Device access type
                                        Regular:
                                                Access type     Value
                                                Read              4
                                                Read and Write    6
                                                Preferred         8

                                        IP:
                                                Access type     Value
                                                Read             20
                                                Read/ Write      22

                                        Fibre Channel (FC)
                                                Access type     Value
                                                Read             36
                                                Read and Write   38

                                        iSCSi
                                                Access type     Value
                                                Read             132
                                                Read and Write   134
        """

        if not all([isinstance(mountpath_id, int), isinstance(device_id, int), isinstance(device_controller_id, int),
                    isinstance(media_agent_id, int), isinstance(device_access_type, int)]):
            raise SDKException('Storage', '101')

        request_json = {
            "EVGui_MMDevicePathInfoReq":
                {
                    "mountpathId": mountpath_id,
                    "infoList": {
                        "accessType": device_access_type,
                        "deviceId": device_id,
                        "deviceControllerId": device_controller_id,
                        "path": self.mount_path,
                        "enabled": 1,
                        "numWriters": -1,
                        "opType": 2,
                        "autoPickTransportType": 0,
                        "protocolType": 679,
                        "mediaAgent": {
                            "id": media_agent_id
                        }
                    }
                }
        }
        self._commcell_object.qoperation_execute(request_json)

    def verify_media(self, media_name, location_id):
        """
            To perform verify media operation on media
            Args:
                media_name  --  Barcode of the media

                location_id --  Slot Id of the media on the library
        """

        if not (isinstance(media_name, basestring) and
                isinstance(location_id,int)):
            raise SDKException('Storage', '101')

        request_xml = f"""<TMMsg_CreateTaskReq>
                            <taskInfo>
                                <task taskType="1" />
                                <subTasks subTaskOperation="1">
                                    <subTask operationType="4005" subTaskType="1"/>
                                    <options>
                                        <adminOpts>
                                            <libraryOption operation="6">
                                                <library _type_="9" libraryName="{self.library_name}"/>
                                                <media _type_="46" mediaName="{media_name}"/>
                                                <verifyMedia>
                                                    <location _type_="53" locationId="{location_id}"/>
                                                </verifyMedia>
                                            </libraryOption>
                                        </adminOpts>
                                    </options>
                                </subTasks>
                            </taskInfo>
                        </TMMsg_CreateTaskReq>"""

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CREATE_TASK'], request_xml
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    from cvpysdk.job import Job
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                if "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Error: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102',o_str)

                else:
                    raise SDKException('Response', '102')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    @property
    def free_space(self):
        """Returns free space"""
        return self._library_properties.get('magLibSummary', {}).get('totalFreeSpace').strip()

    @property
    def mountpath_usage(self):
        """Returns mount path usage"""
        return self._library_properties.get('magLibSummary', {}).get('mountPathUsage').strip()

    @mountpath_usage.setter
    def mountpath_usage(self, value):
        """
            Sets mount path usage on the library
            Args:
                value  (str)   -- option needed to set for mountpath usage
                                    value: 'SPILL_AND_FILL' or 'FILL_AND_SPILL'
        """
        if not isinstance(value, basestring):
            raise SDKException('Storage', '101')

        if value == 'SPILL_AND_FILL':
            value = 1
        elif value == 'FILL_AND_SPILL':
            value = 2
        else:
            raise SDKException('Storage', '110')

        request_json = {
            "EVGui_ConfigureStorageLibraryReq":
                {
                    "library": {
                            "opType": 32,
                            "libraryName": self.library_name
                        },
                    "libNewProp": {
                            "mountPathUsage": value
                        }
                }
        }
        self._commcell_object.qoperation_execute(request_json)

    def set_mountpath_preferred_on_mediaagent(self, value):
        """Sets select preferred mountPath according to mediaagent setting on the library.
            Args:
                value    (bool) --  preferMountPathAccordingToMA value to be set on library (True/False)

            Raises:
                SDKException:
                    if failed to update

                    if the type of value input is not correct

        """
        if not isinstance(value, bool):
            raise SDKException('Storage', '101')

        request_json = {
            "EVGui_ConfigureStorageLibraryReq":
                {
                    "isConfigRequired": 1,
                    "library": {
                            "opType": 32,
                            "libraryName": self.library_name
                        },
                    "libNewProp": {
                            "preferMountPathAccordingToMA": int(value)
                        }
                }
        }
        self._commcell_object.qoperation_execute(request_json)

    @property
    def media_agents_associated(self):
        """Returns the media agents associated with the disk library"""
        media_agents = self._library_properties['magLibSummary'].get(
            'associatedMediaAgents', None)
        if media_agents is None:
            return []
        return media_agents.strip().split(",")

    @property
    def name(self):
        """Returns library display name."""
        return self._library_properties['MountPathList'][0]['mountPathSummary']['libraryName']

    @property
    def library_name(self):
        """Treats the library name as a read-only attribute."""
        return self._library_name

    @property
    def library_id(self):
        """Treats the library id as a read-only attribute."""
        return self._library_id

    @property
    def library_properties(self):
        """Returns the dictionary consisting of the full properties of the library"""
        self.refresh()
        return self._library_properties

    @property
    def mount_path(self):
        """Treats the library id as a read-only attribute."""
        return self.mountpath

    @mount_path.setter
    def mount_path(self, mount_path):
        """ setter for mountpath"""
        self.mountpath = mount_path

    @property
    def media_agent(self):
        """Treats the library id as a read-only attribute."""
        return self.mediaagent

    @media_agent.setter
    def media_agent(self, media_agent):
        """setter for media agent"""
        self.mediaagent = media_agent
        
    def share_mount_path(self, new_media_agent, new_mount_path, **kwargs):
        """
        Method to share a mountpath to a disklibrary

        Args:
        
            new_media_agent (str)   -- Media agent which is accessing the shared mount path
            
            new_mount_path  (int)   -- Mount path to be shared
            
            \*\*kwargs  (dict)  --  Optional arguments

                    Available kwargs Options:
            
                        media_agent     (str)   -- Media agent associated with library
                        
                        library_name    (str)   -- Name of the library which has the mount path
                    
                        mount_path      (str)   -- Mount path to be shared
                        
                        access_type     (int)   -- The access type of the shared mount path

                                                    Read Device Access = 4
                                                    
                                                    Read/ Write Device Access = 6
                                                    
                                                    Read Device Access with Preferred = 12
                                                    
                                                    Read/Write Device Access with Preferred = 14
                                                    
                                                    Data Server - IP Read = 20
                                                    
                                                    Data Server - IP Read/ Write = 22
                                                    
                                                    Data Server - FC Read = 36
                                                    
                                                    Data Server - FC Read/ Write = 38
                                                    
                                                    Data Server - iSCSI Read = 132
                                                    
                                                    Data Server - iSCSI Read/ Write = 134
                                                    
                                                    Note: For the Data Server device access type,
                                                          enter the local path provided in the library/mountPath
                                                          parameter in the libNewProp/mountPath parameter also.
                        

                        username        (str)   -- Username to access the mount path, if UNC

                        password        (str)   -- Password to access the mount path, if UNC

        Returns:
            None

        Raises
            Exception:
                - if any of the parameter's dataype is invalid

                - if API response error code is not 0

                - if response is empty

                - if response code is not as expected
        """
        
        media_agent = kwargs.get('media_agent', self.mediaagent)
        library_name = kwargs.get('library_name', self.library_name)
        mount_path = kwargs.get('mount_path', self.mountpath)
        access_type = kwargs.get('access_type', 22)
        username = kwargs.get('username', '')
        password = kwargs.get('password', '')
       
        self._EXECUTE = self._commcell_object._services['EXECUTE_QCOMMAND']
        self.library = {
            "opType": 64,
            "mediaAgentName": media_agent,
            "libraryName": library_name,
            "mountPath": "%s" %
                         mount_path}
        self.lib_new_prop = {
            "deviceAccessType": access_type,
            "password": password,
            "loginName": username,
            "mediaAgentName": new_media_agent,
            "mountPath": "{}".format(new_mount_path),
            "proxyPassword": ""}
        request_json = {
            "EVGui_ConfigureStorageLibraryReq":
                {
                    "library": self.library,
                    "libNewProp": self.lib_new_prop
                }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._EXECUTE, request_json
        )
        if flag:
            response_string = self._commcell_object._update_response_(response.text)
            if response.json():
                if "library" in response.json():
                    response = response.json()["library"]
                    return response
                else:
                    raise SDKException('Response', '102', response_string)
            else:

                raise SDKException('Response', '102', response_string)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


class RPStores(object):
    def __init__(self, commcell):
        """Initialize object of the MediaAgents class.

            Args:
                commcell(object)  --  instance of the Commcell class

            Returns:
                object - instance of the MediaAgents class
        """
        self._commcell = commcell
        self._rp_stores = None
        self.refresh()

    def _get_rp_stores(self):
        xml = '<?xml version="1.0" encoding="UTF-8"?><EVGui_GetLibraryListWCReq libraryType="RPSTORE"/>'
        response = self._commcell.execute_qcommand("qoperation execute", xml)

        try:
            return {library["library"]["libraryName"].lower(): library["MountPathList"][0]["rpStoreLibraryInfo"]
                    ["rpStoreId"] for library in response.json()["libraryList"]}
        except (KeyError, ValueError):
            generic_msg = "Unable to fetch RPStore"
            err_msg = response.json().get("errorMessage", generic_msg) if response.status_code == 200 else generic_msg
            raise SDKException('Storage', '102', '{0}'.format(err_msg))

    def add(self, name, path, storage, media_agent_name):
        """

        Args:
            name    (str):     Name of the RPStore

            path    (str):     Path of the RPStore

            storage (int):     Storage Capacity of the RPStore in GB

            media_agent_name(str)   :   Name of the media agent

        Returns:
            An instance of RPStore

        """
        try:
            assert self.has_rp_store(name) is False
        except AssertionError:
            raise SDKException("Storage", 102, "An RPStore already exists with the same name")

        media_agents = MediaAgents(self._commcell)
        try:
            ma_id = media_agents.all_media_agents[media_agent_name]["id"]
        except KeyError:
            raise SDKException('Storage', '102', 'No media agent exists with name: {0}'.format(media_agent_name))

        payload = {
            "rpLibrary": {"maxSpacePerRPStoreGB": storage},
            "storageLibrary": {
                "mediaAgentId": int(ma_id),
                "libraryName": name,
                "mountPath": path
            },
            "opType": 1
        }
        flag, response = self._commcell._cvpysdk_object.make_request(
            "POST", self._commcell._services["RPSTORE"], payload)

        try:
            return RPStore(self._commcell, name, response.json()["storageLibrary"]["libraryId"])
        except KeyError:
            generic_msg = "Unable to add RPStore"
            err_msg = response.json().get("errorMessage", generic_msg) if flag else generic_msg
            raise SDKException('Storage', '102', '{0}'.format(err_msg))

    def has_rp_store(self, rpstore_name):
        """Validates if the given RPStore is present

        Args:
            rpstore_name       (str):   Name of the RPStore

        Returns:
            bool : True if present else False
        """
        if not isinstance(rpstore_name, basestring):
            raise SDKException('Storage', '101')

        return rpstore_name.lower() in self._rp_stores

    def get(self, rpstore_name):
        """Fetches the given RPStore

        Args:
            rpstore_name    (str):  Name of the RPStore

        Returns:
            An instance of the RPStore

        """
        if not isinstance(rpstore_name, basestring):
            raise SDKException('Storage', '101')

        try:
            return RPStore(self._commcell, rpstore_name, self._rp_stores[rpstore_name.lower()])
        except KeyError:
            raise SDKException('Storage', '102', 'No RPStore exists with name: {0}'.format(rpstore_name))

    def refresh(self):
        """Refresh the media agents associated with the Commcell."""
        self._rp_stores = self._get_rp_stores()


class RPStore(object):
    def __init__(self, commcell, rpstore_name, rpstore_id):
        self._commcell = commcell
        self._rpstore_name = rpstore_name.lower()
        self._rpstore_id = rpstore_id

    @property
    def rpstore_name(self):
        return self._rpstore_name

    @property
    def rpstore_id(self):
        return self._rpstore_id
