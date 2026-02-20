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

    set_ransomware_protection()  -- set / unset ransomware protection on Windows MA

    set_concurrent_lan()        --  set / unset concurrent LAN backup in Media agent properties.

    is_power_management_enabled() -- returns of power management is enabled or not

Libraries:

    __init__()               --  initialize the instance of Libraries class

    _get_libraries           --  Gets all the libraries associated to the commcell specified by commcell object

    has_library              --  Checks if a library exists in the commcell with the input library name

    refresh                  --  Refresh the libraries associated with the Commcell


DiskLibraries:
    __init__(commcell_object)   --  initialize the DiskLibraries class instance for the commcell

    __str__()                   --  returns all the disk libraries associated with the commcell

    __repr__()                  --  returns the string for the instance of the DiskLibraries class

    all_disk_libraries()        --  returns the dict of all the disk libraries on commcell

    add()                       --  adds a new disk library to the commcell

    delete()                    --  Deletes a disk library from commcell

    get(library_name)           --  returns the instance of the DiskLibrary class
    for the library specified


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

    add_storage_accelerator_credential() -- Add storage accelerator credential to the cloud mount path

    add_mount_path()            --  adds the mount path on the local/ remote machine

    delete_mount_path()         -- Deletes the mount path on the local / remote machine

    set_mountpath_reserve_space()      --  to set reserve space on the mountpath

    set_max_data_to_write_on_mount_path()  -- to set max data to write on the mountpath

    change_device_access_type()  -- to change device access type

    modify_cloud_access_type()   -- To change device access type for cloud mount path

    update_device_controller()   -- To update device controller properties.

    verify_media()              --  To perform verify media operation on media

    set_mountpath_preferred_on_mediaagent() --  Sets select preferred mountPath according to mediaagent setting on the
                                                library

    _get_library_properties()   --  gets the disk library properties

    _get_advanced_library_properties() --  gets the advanced disk library  properties
    
    refresh()                   --  Refresh the properties of this disk library.

DiskLibrary instance Attributes

    **media_agents_associated**     --  returns the media agents associated with the disk library
    **library_properties**          --  Returns the dictionary consisting of the full properties of the library
    **advanced_library_properties** -- Returns the dictionary consisting of advanced library properites
    **free_space**                  --  returns the free space on the library
    **mountpath_usage**             --  returns mountpath usage on library

TapeLibraries:

    __init__()    --  initialize the TapeLibrary class instance for the commcell

    get()                        --  Returns the TapeLibrary object of the specified library

    delete()                     --  Deletes the specified library

    lock_mm_configuration()      --  Locks the MM config for tape library detection

    unlock_mm_configuration()    --  Unlocks the MM config for tape library detection

    __lock_unlock_mm_configuration()    --  Locks or unlocks the MM config for tape library detection

    detect_tape_library()        --  Detect the tape library of the specified MediaAgent(s)

    configure_tape_library()     --  Configure the specified tape library


TapeLibrary:

     __init__()         --  Initialize the TapeLibrary class instance

     __repr__           --  returns the string for the instance of the TapeLibrary class

     _get_library_id()  --  Returns the library ID

     _get_library_properties()   --  gets the disk library properties

     get_drive_list()   --  Returns the tape drive list of this tape library

     refresh()          --  Refresh the properties of this tape library.

    verify_media_status()                     --  Verify media status
    _process_media_details()                   --  fetch required details and sets media details class variable.
    _get_all_media_details()                   --  fetch all media details. 
    _get_media_id_list()                       --  return media Ids for the given barcode media names.
    _perform_media_operations()                --  common function to perform media operations 

    get_media_status()                        --  return media status for the given media barcode.
    mark_media_appendable()                   --  mark the given list of media appendable.
    mark_media_full()                         --  mark the given list of media full.


"""

from __future__ import absolute_import
from __future__ import unicode_literals
import json, time, uuid
from base64 import b64encode
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from .exception import SDKException

if TYPE_CHECKING:
    from .job import Job
    from .commcell import Commcell

class MediaAgents(object):
    """
    Manages and interacts with media agents associated with a CommCell.

    This class provides an interface to retrieve, manage, and manipulate media agents
    within a CommCell environment. It allows users to query all available media agents,
    check for the existence of specific media agents, retrieve details, delete agents,
    and refresh the media agent list. The class is initialized with a CommCell object
    and offers convenient string representations for debugging and logging.

    Key Features:
        - Retrieve all media agents associated with the CommCell
        - Check if a specific media agent exists
        - Get details of a specific media agent
        - Delete a media agent with optional force deletion
        - Refresh the list of media agents from the CommCell
        - Access all media agents via a property
        - String and representation methods for easy inspection

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a MediaAgents object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> media_agents = MediaAgents(commcell)
            >>> print("MediaAgents object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._MEDIA_AGENTS = self._commcell_object._services['GET_MEDIA_AGENTS']
        self._media_agents = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all media agents associated with the Commcell.

        This method provides a human-readable summary listing all media agents managed by the Commcell.

        Returns:
            A string containing the names or details of all media agents.

        Example:
            >>> media_agents = MediaAgents(commcell_object)
            >>> print(str(media_agents))
            MediaAgent1, MediaAgent2, MediaAgent3
        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Media Agent')

        for index, media_agent in enumerate(self._media_agents):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, media_agent)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the MediaAgents instance.

        This method provides a developer-friendly string that represents the current
        MediaAgents object, useful for debugging and logging purposes.

        Returns:
            A string representation of the MediaAgents instance.

        Example:
            >>> media_agents = MediaAgents(commcell_object)
            >>> print(repr(media_agents))
            <MediaAgents object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        return "MediaAgents class instance for Commcell"

    def _get_media_agents(self) -> dict:
        """Retrieve all media agents associated with the Commcell.

        Returns:
            dict: A dictionary containing all media agents of the Commcell, where each key is the media agent's name,
            and the value is a dictionary with the following details:
                - 'id': The unique identifier of the media agent.
                - 'os_info': The operating system information of the media agent.
                - 'is_online': The online status of the media agent (bool).

            Example structure:
                {
                    "media_agent1_name": {
                        "id": 123,
                        "os_info": "Windows Server 2019",
                        "is_online": True
                    },
                    "media_agent2_name": {
                        "id": 456,
                        "os_info": "Linux CentOS 7",
                        "is_online": False
                    }
                }

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> media_agents = media_agents_obj._get_media_agents()
            >>> for name, details in media_agents.items():
            ...     print(f"Media Agent: {name}, ID: {details['id']}, Online: {details['is_online']}")
        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._MEDIA_AGENTS
        )

        if flag:
            if isinstance(response.json(), dict):
                media_agents = response.json().get('mediaAgentList', [])
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
    def all_media_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all media agents available on this Commcell.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary where each key is a media agent name, and the value is a dictionary
            containing details about that media agent, such as its ID, operating system information, and online status.
            Example structure:
                {
                    "media_agent1_name": {
                        "id": media_agent1_id,
                        "os_info": media_agent1_os,
                        "is_online": media_agent1_status
                    },
                    "media_agent2_name": {
                        "id": media_agent2_id,
                        "os_info": media_agent2_os,
                        "is_online": media_agent2_status
                    }
                }

        Example:
            >>> media_agents = commcell_obj.media_agents.all_media_agents
            >>> for name, details in media_agents.items():
            ...     print(f"Media Agent: {name}, ID: {details['id']}, Online: {details['is_online']}")

        #ai-gen-doc
        """
        return self._media_agents

    def has_media_agent(self, media_agent_name: str) -> bool:
        """Check if a media agent with the specified name exists in the Commcell.

        Args:
            media_agent_name: The name of the media agent to check for existence.

        Returns:
            True if the media agent exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the media_agent_name argument is not a string.

        Example:
            >>> media_agents = MediaAgents(commcell_object)
            >>> exists = media_agents.has_media_agent("MediaAgent01")
            >>> print(f"Media agent exists: {exists}")
            # Output: Media agent exists: True

        #ai-gen-doc
        """
        if not isinstance(media_agent_name, str):
            raise SDKException('Storage', '101')

        return self._media_agents and media_agent_name.lower() in self._media_agents

    def get(self, media_agent_name: str) -> 'MediaAgent':
        """Retrieve a MediaAgent object by its name.

        Args:
            media_agent_name: The name of the media agent to retrieve.

        Returns:
            MediaAgent: An instance of the MediaAgent class corresponding to the specified name.

        Raises:
            SDKException: If the media_agent_name is not a string, or if no media agent exists with the given name.

        Example:
            >>> media_agents = MediaAgents(commcell_object)
            >>> ma = media_agents.get("MediaAgent01")
            >>> print(f"Retrieved media agent: {ma}")
            >>> # The returned MediaAgent object can be used for further operations

        #ai-gen-doc
        """
        if not isinstance(media_agent_name, str):
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

    def delete(self, media_agent: str, force: bool = False) -> None:
        """Delete a media agent from the Commcell.

        Args:
            media_agent: The name of the media agent to remove from the Commcell.
            force: If True, deletes the media agent forcefully. Defaults to False.

        Raises:
            SDKException: If the media agent name is not a string, if the deletion fails,
                if the response is empty or unsuccessful, or if no media agent exists with the given name.

        Example:
            >>> media_agents = MediaAgents(commcell_object)
            >>> media_agents.delete('MediaAgent01')
            >>> # To forcefully delete a media agent:
            >>> media_agents.delete('MediaAgent01', force=True)

        #ai-gen-doc
        """
        if not isinstance(media_agent, str):
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

    def refresh(self) -> None:
        """Reload the list of media agents associated with the Commcell.

        This method clears any cached media agent data, ensuring that subsequent accesses
        retrieve the most up-to-date information from the Commcell.

        Example:
            >>> media_agents = MediaAgents(commcell_object)
            >>> media_agents.refresh()  # Refresh the media agent list
            >>> print("Media agents refreshed successfully")

        #ai-gen-doc
        """
        self._media_agents = self._get_media_agents()


class MediaAgent(object):
    """
    Represents a specific media agent within a CommCell environment.

    This class provides comprehensive management and configuration capabilities for a media agent,
    including power management, index cache operations, maintenance mode, ransomware protection,
    and concurrent LAN settings. It exposes properties to access key media agent attributes and
    offers methods to perform power operations, update configurations, and refresh the agent's state.

    Key Features:
        - Initialization and representation of media agent objects
        - Retrieval and management of media agent properties and IDs
        - Power management operations: enable, power on/off, wait for status, and perform operations
        - Index cache path management and configuration
        - Enable/disable media agent state and maintenance mode
        - Ransomware protection configuration
        - Enable/disable concurrent LAN operations
        - Access to media agent properties such as name, ID, online status, platform, index cache details, and power status
        - Refreshing media agent properties to reflect current state

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', media_agent_name: str, media_agent_id: int = None) -> None:
        """Initialize a MediaAgent object.

        Args:
            commcell_object: An instance of the Commcell class representing the connected Commcell.
            media_agent_name: The name of the media agent to manage.
            media_agent_id: Optional; the unique identifier of the media agent. If not provided, it will be determined automatically.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> media_agent = MediaAgent(commcell, 'MediaAgent01')
            >>> # The MediaAgent object is now initialized and ready for use

        #ai-gen-doc
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

    def __repr__(self) -> str:
        """Return the string representation of the MediaAgent instance.

        This method provides a developer-friendly string that identifies the MediaAgent object,
        typically including relevant details for debugging or logging purposes.

        Returns:
            A string representation of the MediaAgent instance.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> print(repr(media_agent))
            >>> # Output might look like: <MediaAgent: MediaAgent01>

        #ai-gen-doc
        """
        representation_string = 'MediaAgent class instance for MA: "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self.media_agent_name, self._commcell_object.commserv_name
        )

    def _get_media_agent_id(self) -> str:
        """Retrieve the unique identifier associated with this media agent.

        Returns:
            The media agent ID as a string.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> media_agent_id = media_agent._get_media_agent_id()
            >>> print(f"Media Agent ID: {media_agent_id}")

        #ai-gen-doc
        """
        media_agents = MediaAgents(self._commcell_object)
        return media_agents.get(self.media_agent_name).media_agent_id

    def _get_media_agent_properties(self) -> dict:
        """Retrieve the properties of the current media agent.

        Returns:
            dict: A dictionary containing the properties of this media agent.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> properties = media_agent._get_media_agent_properties()
            >>> print(properties)
            >>> # Access specific property
            >>> agent_name = properties.get('mediaAgent', {}).get('mediaAgentName')
            >>> print(f"Media Agent Name: {agent_name}")

        #ai-gen-doc
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

    def _initialize_media_agent_properties(self) -> None:
        """Initialize the properties for this MediaAgent instance.

        This method sets up or refreshes the internal properties associated with the MediaAgent object.
        It is typically called internally to ensure that the MediaAgent's state is up to date.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> media_agent._initialize_media_agent_properties()
            >>> # The MediaAgent's properties are now initialized and ready for use

        #ai-gen-doc
        """
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

        if mediaagent_list['mediaAgentProps']['indexLogsCacheInfo']['logsCachePath']['path']:
            self._index_cache = mediaagent_list['mediaAgentProps']['indexLogsCacheInfo'
                                                                   ]['logsCachePath']['path']

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

    def enable_power_management(self, pseudo_client_name: str) -> None:
        """Enable power management for the MediaAgent using the specified cloud controller.

        This method enables power management features by associating the MediaAgent with a
        Virtual Server Agent (VSA) pseudo client, which acts as the cloud controller.

        Args:
            pseudo_client_name: The name of the VSA pseudo client to be used as the cloud controller.

        Raises:
            SDKException: If the response is not successful or if power management is not supported.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.enable_power_management("CloudControllerPseudoClient")
            >>> print("Power management enabled successfully.")

        #ai-gen-doc
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

    def _perform_power_operation(self, operation: int) -> None:
        """Perform a power operation on the MediaAgent.

        This method initiates a power management operation (such as power on or power off)
        on the MediaAgent, depending on the value of the `operation` parameter.

        Args:
            operation: The power operation to perform. Typically, 1 for power on and 0 for power off.

        Raises:
            SDKException: If the operation value is not 1 or 0.
            SDKException: If power management is not enabled or not supported on the MediaAgent.
            SDKException: If the API response is empty.
            SDKException: If the API response indicates failure.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent._perform_power_operation(1)  # Power on the MediaAgent
            >>> media_agent._perform_power_operation(0)  # Power off the MediaAgent

        #ai-gen-doc
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

    def power_on(self, wait_till_online: bool = True) -> None:
        """Power on the MediaAgent.

        This method initiates the power-on sequence for the MediaAgent. By default, it waits until the MediaAgent is fully online before returning. If `wait_till_online` is set to False, the method submits the power-on request and returns immediately without waiting for the MediaAgent to become online.

        Args:
            wait_till_online: 
                If True (default), waits until the MediaAgent is online before returning.
                If False, submits the power-on request and returns immediately.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.power_on()  # Waits until the MediaAgent is online
            >>> media_agent.power_on(wait_till_online=False)  # Submits request and returns immediately

        #ai-gen-doc
        """

        if self.current_power_status not in ["Starting", "Started", "Online"]:
            self._perform_power_operation("1")

        if wait_till_online == True and self.current_power_status != "Online":
            self.wait_for_power_status("Online")

    def power_off(self, wait_till_stopped: bool = True) -> None:
        """Power off the MediaAgent.

        This method initiates a power-off operation for the MediaAgent. By default, it waits until the MediaAgent is fully stopped before returning. If `wait_till_stopped` is set to False, the method submits the power-off request and returns immediately.

        Args:
            wait_till_stopped: 
                If True (default), waits until the MediaAgent is stopped before returning.
                If False, submits the power-off request and returns immediately.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.power_off()  # Waits until the MediaAgent is stopped
            >>> media_agent.power_off(wait_till_stopped=False)  # Submits request and returns immediately

        #ai-gen-doc
        """

        if self.current_power_status not in ["Stopping", "Stopped"]:
            self._perform_power_operation("0")

        if wait_till_stopped == True and self.current_power_status != "Stopped":
            self.wait_for_power_status("Stopped")

    def wait_for_power_status(self, expected_power_status: str, time_out_sec: int = 600) -> None:
        """Wait until the MediaAgent reaches the specified power status or the timeout is reached.

        This method blocks execution until the MediaAgent's power status matches the expected value,
        or until the specified timeout period elapses.

        Args:
            expected_power_status: The desired power status to wait for. Valid values include:
                - "Starting"
                - "Started"
                - "Online"
                - "Stopping"
                - "Stopped"
            time_out_sec: Maximum number of seconds to wait for the expected power status. Defaults to 600 seconds.

        Raises:
            SDKException: If `time_out_sec` is not an integer and not None, or if the expected power status
                is not achieved within the specified timeout period.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.wait_for_power_status("Online", time_out_sec=300)
            >>> print("MediaAgent is now online.")

        #ai-gen-doc
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

    def change_index_cache(self, old_index_cache_path: str, new_index_cache_path: str, 
                           logs_cache_enabled: bool = False, logs_cache_path: Optional[str] = None) -> 'Job':
        """Initiate a catalog migration job to move the index cache from one path to another.

        This method starts a catalog migration job using the CreateTask endpoint, migrating the index cache 
        from the specified source path to the destination path on the MediaAgent.

        Args:
            old_index_cache_path: The current (source) index cache path to migrate from.
            new_index_cache_path: The new (destination) index cache path to migrate to.
            logs_cache_enabled: If True, enables logs cache. Defaults to False.
            logs_cache_path: Optional; the path for logs cache if `logs_cache_enabled` is True.

        Returns:
            Job: An object representing the catalog migration job.

        Raises:
            SDKException: If the response from the CreateTask endpoint is empty or indicates failure.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> job = media_agent.change_index_cache("/old/cache/path", "/new/cache/path")
            >>> print(f"Migration job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not logs_cache_path or not isinstance(logs_cache_path, str):
            logs_cache_path = old_index_cache_path

        media_id = int(self.media_agent_id)
        request_json = {
            "mediaAgentInfo": {
                "mediaAgent": {
                    "mediaAgentId": media_id
                },
                "mediaAgentProps": {
                    "indexDirectory": {
                        "path": new_index_cache_path
                    },
                    "indexLogsCacheInfo": {
                        "isEnabled": logs_cache_enabled,
                        "logsCachePath": {
                            "path": logs_cache_path
                        }
                    }
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._MEDIA_AGENTS, request_json
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

    def set_state(self, enable: bool = True) -> None:
        """Enable or disable the media agent by updating its properties.

        Args:
            enable: If True, enables the media agent; if False, disables it. Defaults to True.

        Raises:
            Exception: If there is an empty response, an error during request execution, or if the response status indicates failure.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.set_state(enable=False)  # Disables the media agent
            >>> media_agent.set_state(enable=True)   # Enables the media agent

        #ai-gen-doc
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


    def mark_for_maintenance(self, mark: bool = False) -> None:
        """Mark or unmark the MediaAgent for maintenance mode.

        This method sets the MediaAgent to maintenance mode (offline) or removes it from maintenance mode,
        depending on the value of the `mark` parameter.

        Args:
            mark: 
                True to mark the MediaAgent for maintenance (offline).
                False to unmark the MediaAgent and bring it back online.

        Raises:
            Exception: If there is an empty response, an error during request execution, or if the response status indicates failure.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.mark_for_maintenance(True)   # Mark the MediaAgent for maintenance
            >>> media_agent.mark_for_maintenance(False)  # Unmark the MediaAgent for maintenance

        #ai-gen-doc
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

    def set_ransomware_protection(self, status: bool) -> None:
        """Enable or disable ransomware protection on a Windows MediaAgent.

        This method allows you to turn ransomware protection on or off for the specified MediaAgent.
        Set `status` to True to enable protection, or False to disable it.

        Args:
            status: Set to True to enable ransomware protection, or False to disable it.

        Raises:
            Exception: If there is a failure in executing the operation.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.set_ransomware_protection(True)   # Enable ransomware protection
            >>> media_agent.set_ransomware_protection(False)  # Disable ransomware protection

        #ai-gen-doc
        """
        # this works only on WINDOWS MA
        if self._platform != 'WINDOWS':
            raise SDKException('Storage', '101')

        if type(status) != bool:
            raise SDKException('Storage', '101')

        media_id = int(self.media_agent_id)

        request_json = {
            "mediaAgentInfo": {
                "mediaAgent": {
                    "mediaAgentId": media_id
                },
                "mediaAgentProps": {
                    "isRansomwareProtected": status
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

    def set_concurrent_lan(self, enable: bool = True) -> None:
        """Enable or disable concurrent LAN backup in the Media Agent properties.

        Args:
            enable: If True, enables concurrent LAN backup. If False, disables it.

        Raises:
            SDKException: If there is a failure in executing the operation.

        Example:
            >>> media_agent = MediaAgent()
            >>> media_agent.set_concurrent_lan(enable=True)   # Enable concurrent LAN backup
            >>> media_agent.set_concurrent_lan(enable=False)  # Disable concurrent LAN backup

        #ai-gen-doc
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
                    "optimizeForConcurrentLANBackups": enable
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
    def name(self) -> str:
        """Get the display name of the MediaAgent.

        Returns:
            The display name of the MediaAgent as a string.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> print(media_agent.name)
            MediaAgent01

        #ai-gen-doc
        """
        return self._media_agent_info['mediaAgent']['displayName']

    @property
    def media_agent_name(self) -> str:
        """Get the name of the media agent as a read-only property.

        Returns:
            The name of the media agent as a string.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> name = media_agent.media_agent_name  # Access the property
            >>> print(f"Media agent name: {name}")

        #ai-gen-doc
        """
        return self._media_agent_name

    @property
    def media_agent_id(self) -> str:
        """Get the unique identifier of the MediaAgent as a read-only property.

        Returns:
            str: The unique ID associated with this MediaAgent.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent1")
            >>> agent_id = media_agent.media_agent_id  # Access the media agent ID
            >>> print(f"MediaAgent ID: {agent_id}")

        #ai-gen-doc
        """
        return self._media_agent_id

    @property
    def is_online(self) -> bool:
        """Check if the MediaAgent is currently online.

        Returns:
            True if the MediaAgent is online, False otherwise.

        Example:
            >>> media_agent = MediaAgent()
            >>> if media_agent.is_online:
            ...     print("MediaAgent is online")
            ... else:
            ...     print("MediaAgent is offline")

        #ai-gen-doc
        """
        return self._is_online

    @property
    def platform(self) -> str:
        """Get the platform type of the MediaAgent as a read-only attribute.

        Returns:
            The platform type of the MediaAgent (e.g., 'Windows', 'Linux') as a string.

        Example:
            >>> media_agent = MediaAgent(commcell_object, 'MediaAgent001')
            >>> print(media_agent.platform)
            Windows

        #ai-gen-doc
        """
        return self._platform

    @property
    def index_cache_path(self) -> str:
        """Get the index cache path for the MediaAgent as a read-only property.

        Returns:
            The file system path to the index cache directory used by the MediaAgent.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> cache_path = media_agent.index_cache_path
            >>> print(f"Index cache path: {cache_path}")

        #ai-gen-doc
        """
        return self._index_cache

    @property
    def index_cache_enabled(self) -> bool:
        """Indicate whether the index cache is enabled for this MediaAgent.

        Returns:
            bool: True if the index cache is enabled, False otherwise.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent1")
            >>> is_enabled = media_agent.index_cache_enabled
            >>> print(f"Index cache enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._index_cache_enabled

    @property
    def is_power_management_enabled(self) -> bool:
        """Check if power management is enabled for the MediaAgent.

        Returns:
            bool: True if power management is enabled, False otherwise.

        Example:
            >>> media_agent = MediaAgent()
            >>> if media_agent.is_power_management_enabled:
            ...     print("Power management is enabled.")
            ... else:
            ...     print("Power management is disabled.")

        #ai-gen-doc
        """
        return self._is_power_management_enabled

    @property
    def current_power_status(self) -> str:
        """Get the current power status of the MediaAgent.

        Returns:
            The current power status of the MediaAgent as a string. Possible values include:
                - "Starting": Power-on process is in progress.
                - "Started": MediaAgent is powered on but not yet synced with the CommServe.
                - "Online": Powered on and synced with the CommServe; MediaAgent is ready to use.
                - "Stopping": Power-off operation is in progress.
                - "Stopped": MediaAgent is powered off.
                - "Unknown": Power status is not yet synced with the cloud provider, discovery is ongoing, or there is an issue.

        Example:
            >>> ma = MediaAgent()
            >>> status = ma.current_power_status
            >>> print(f"MediaAgent power status: {status}")
            # Output might be: MediaAgent power status: Online

        #ai-gen-doc
        """
        self.refresh()
        power_status = {0: 'Unknown', 1: 'Starting', 2: 'Started', 3: 'Online', 4: 'Stopping', 5: 'Stopped'}
        return power_status.get(self._power_status)

    def refresh(self) -> None:
        """Reload the properties of the MediaAgent to ensure the latest information is available.

        This method updates the MediaAgent's internal state by fetching the most recent properties
        from the Commcell or associated data source. Use this method when you suspect that the
        MediaAgent's properties may have changed externally and need to be synchronized.

        Example:
            >>> media_agent = MediaAgent(commcell_object, "MediaAgent01")
            >>> media_agent.refresh()  # Refreshes the MediaAgent's properties
            >>> print("MediaAgent properties updated successfully")

        #ai-gen-doc
        """
        self._initialize_media_agent_properties()


class Libraries(object):
    """
    Class for managing and interacting with libraries within a CommCell environment.

    This class provides functionality to retrieve, check, and refresh library information.
    It is initialized with a CommCell object and offers methods to access the current
    libraries, verify the existence of a specific library, and update the library list.

    Key Features:
        - Initialization with a CommCell object for context
        - Retrieval of all available libraries
        - Check for the existence of a library by name
        - Refresh and update the internal library list

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize an instance of the DiskLibraries class with a Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> disk_libraries = Libraries(commcell)
            >>> print("DiskLibraries object initialized:", disk_libraries)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._LIBRARY = self._commcell_object._services['LIBRARY']

        self._libraries = None
        self.refresh()

    def _get_libraries(self) -> Dict[str, int]:
        """Retrieve all disk libraries associated with the Commcell.

        Returns:
            A dictionary mapping disk library names to their corresponding IDs.
            Example:
                {
                    "disk_library1_name": 12345,
                    "disk_library2_name": 67890
                }

        Raises:
            SDKException: If the response from the Commcell is empty or unsuccessful.

        Example:
            >>> libraries = Libraries(commcell_object)
            >>> disk_libs = libraries._get_libraries()
            >>> print(disk_libs)
            >>> # Output: {'LibraryA': 101, 'LibraryB': 102}

        #ai-gen-doc
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


    def has_library(self, library_name: str) -> bool:
        """Check if a library with the specified name exists in the Commcell.

        Args:
            library_name: The name of the library to check for existence.

        Returns:
            True if the library exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the library_name argument is not a string.

        Example:
            >>> libraries = Libraries(commcell_object)
            >>> exists = libraries.has_library("TapeLibrary01")
            >>> print(f"Library exists: {exists}")
            # Output: Library exists: True

        #ai-gen-doc
        """
        if not isinstance(library_name, str):
            raise SDKException('Storage', '101')

        return self._libraries and library_name.lower() in self._libraries

    def refresh(self) -> None:
        """Reload the disk libraries information associated with the Commcell.

        This method clears any cached disk library data, ensuring that subsequent accesses
        retrieve the latest information from the Commcell.

        Example:
            >>> libraries = Libraries(commcell_object)
            >>> libraries.refresh()  # Refresh disk library data
            >>> print("Disk libraries have been refreshed.")
            >>> # The next access to disk libraries will fetch updated information

        #ai-gen-doc
        """
        self._libraries = self._get_libraries()


class DiskLibraries(Libraries):
    """
    Manages disk libraries associated with a CommCell environment.

    The DiskLibraries class provides an interface for interacting with all disk libraries
    configured within a CommCell. It allows users to retrieve, add, and delete disk libraries,
    as well as access detailed information about each library. This class is intended to be
    used as part of the CommCell management suite, enabling streamlined disk library operations.

    Key Features:
        - Retrieve all disk libraries associated with the CommCell
        - Add new disk libraries with specified configuration parameters
        - Delete existing disk libraries by name
        - Get detailed information about a specific disk library
        - Provides string representations for easy inspection

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize the DiskLibraries class with a Commcell connection object.

        Args:
            commcell_object: The Commcell object representing the active Commcell session.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> disk_libraries = DiskLibraries(commcell)
            >>> print("DiskLibraries object initialized successfully")

        #ai-gen-doc
        """
        super().__init__(commcell_object)

    def __str__(self) -> str:
        """Return a string representation of all disk libraries associated with the Commcell.

        This method provides a human-readable summary listing all disk libraries managed by the Commcell.

        Returns:
            A string containing the names or details of all disk libraries.

        Example:
            >>> disk_libraries = DiskLibraries(commcell_object)
            >>> print(str(disk_libraries))
            >>> # Output will display all disk libraries associated with the Commcell

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Disk Library')

        for index, library in enumerate(self._libraries):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, library)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the DiskLibraries instance.

        This method provides a developer-friendly string that represents the current
        DiskLibraries object, which can be useful for debugging and logging purposes.

        Returns:
            A string representation of the DiskLibraries instance.

        Example:
            >>> disk_libraries = DiskLibraries(commcell_object)
            >>> print(repr(disk_libraries))
            <DiskLibraries object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        return "DiskLibraries class instance for Commcell"

    @property
    def all_disk_libraries(self) -> Dict[str, int]:
        """Get a dictionary of all disk libraries available on this Commcell.

        Returns:
            Dict[str, int]: A dictionary mapping disk library names to their corresponding IDs.
                Example format:
                    {
                        "disk_library1_name": 123,
                        "disk_library2_name": 456
                    }

        Example:
            >>> disk_libraries = DiskLibraries(commcell_object)
            >>> all_libs = disk_libraries.all_disk_libraries
            >>> print(all_libs)
            {'LibraryA': 101, 'LibraryB': 102}

        #ai-gen-doc
        """
        return self._libraries

    def add(
        self,
        library_name: str,
        media_agent: 'Union[str, MediaAgent]',
        mount_path: str,
        username: str = "",
        password: str = "",
        servertype: int = 0,
        saved_credential_name: str = "",
        **kwargs: Any
    ) -> 'DiskLibrary':
        """Add a new Disk Library to the Commcell.

        This method creates a new disk library on the specified media agent with the given mount path and credentials.
        Additional options can be provided via keyword arguments.

        Args:
            library_name: Name of the new disk library to add.
            media_agent: Name (str) or MediaAgent object representing the media agent to which the library will be added.
            mount_path: Full path of the folder to mount the library at.
            username: Username to access the mount path. Defaults to an empty string.
            password: Password to access the mount path. Defaults to an empty string.
            servertype: Cloud library server type. Defaults to 0. Use 59 for HPstore.
            saved_credential_name: Name of the saved credential to use. Defaults to an empty string.
            **kwargs: Optional keyword arguments. Supported options include:
                - proxy_password (str): Plain text password of the proxy server.

        Returns:
            DiskLibrary: An instance of the DiskLibrary class if the library is created successfully.

        Raises:
            SDKException: If any of the following conditions occur:
                - The type of library_name, mount_path, username, or password is not str.
                - The type of media_agent is not str or MediaAgent instance.
                - Failed to create the disk library.
                - The response is empty or not successful.

        Example:
            >>> disk_libraries = DiskLibraries(commcell_object)
            >>> new_library = disk_libraries.add(
            ...     library_name="BackupDisk01",
            ...     media_agent="MediaAgent01",
            ...     mount_path="/mnt/backup/disk01",
            ...     username="storage_user",
            ...     password="secure_password"
            ... )
            >>> print(f"Created disk library: {new_library}")

        #ai-gen-doc
        """
        if not (isinstance(library_name, str) and
                isinstance(mount_path, str) and
                isinstance(username, str) and
                isinstance(password, str)):
            raise SDKException('Storage', '101')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, str):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        else:
            raise SDKException('Storage', '103')

        proxy_password = kwargs.get('proxy_password', '')

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

            if proxy_password != "":
                request_json["library"]["proxyPassword"] = b64encode(proxy_password.encode()).decode()

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

    def delete(self, library_name: str) -> None:
        """Delete the specified disk library by name.

        Args:
            library_name: The name of the disk library to delete.

        Raises:
            SDKException: If the library_name is not a string, if no library exists with the given name, 
                or if the response from the server is incorrect.

        Example:
            >>> disk_libraries = DiskLibraries(commcell_object)
            >>> disk_libraries.delete("ArchiveLibrary01")
            >>> print("Library deleted successfully.")

        #ai-gen-doc
        """
        if not isinstance(library_name, str):
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

    def get(self, library_name: str, library_details: Optional[dict] = None) -> 'DiskLibrary':
        """Retrieve a DiskLibrary object for the specified disk library name.

        Args:
            library_name: The name of the disk library to retrieve.
            library_details: Optional dictionary containing additional details such as mountpath and mediaagent.

        Returns:
            DiskLibrary: An instance of the DiskLibrary class corresponding to the given library name.

        Raises:
            SDKException: If the library_name is not a string or if no disk library exists with the given name.

        Example:
            >>> disk_libraries = DiskLibraries(commcell_object)
            >>> library = disk_libraries.get("PrimaryDiskLibrary")
            >>> print(f"Retrieved disk library: {library}")
            >>> # Optionally, provide additional details
            >>> details = {"mountpath": "/mnt/disk1", "mediaagent": "MediaAgent01"}
            >>> library_with_details = disk_libraries.get("PrimaryDiskLibrary", library_details=details)

        #ai-gen-doc
        """
        if not isinstance(library_name, str):
            raise SDKException('Storage', '101')
        else:
            library_name = library_name.lower()

            if self.has_library(library_name):
                return DiskLibrary(self._commcell_object,
                                   library_name,
                                   self._libraries[library_name], library_details)

            raise SDKException(
                'Storage', '102', 'No disk library exists with name: {0}'.format(library_name)
            )



class DiskLibrary(object):
    """
    DiskLibrary provides comprehensive management and configuration capabilities for a specific disk library.

    This class enables users to interact with disk libraries, manage mount paths, configure cloud and storage accelerator credentials,
    and perform advanced device and media operations. It exposes properties for accessing library details, mount path usage, free space,
    associated media agents, and more. The class supports both local and cloud mount path management, device access type modifications,
    and media verification.

    Key Features:
        - Initialization with commcell object and library details
        - Move, validate, add, and share mount paths (local and cloud)
        - Add and manage cloud and storage accelerator credentials
        - Set mount path reserve space and maximum data write limits
        - Change and update device access types and controllers
        - Modify cloud access types for mount paths
        - Verify media within the library
        - Refresh and retrieve library properties (basic and advanced)
        - Access properties for free space, mount path usage, associated media agents, library name, ID, and details
        - Set mount path preferences on media agents

    This class is intended for use in environments where disk library management and automation are required, providing a robust interface
    for storage administrators and automation scripts.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', library_name: str, library_id: Optional[int] = None, library_details: Optional[dict] = None) -> None:
        """Initialize a DiskLibrary object representing a disk library in the Commcell.

        Args:
            commcell_object: Instance of the Commcell class used to interact with the Commcell environment.
            library_name: Name of the disk library to be managed.
            library_id: Optional; unique identifier of the disk library. If not provided, it may be determined automatically.
            library_details: Optional; dictionary containing additional details such as mountpath and media agent information.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> disk_library = DiskLibrary(commcell, 'MyDiskLibrary')
            >>> # Optionally, provide library_id and library_details
            >>> details = {'mountpath': '/data/library', 'mediaagent': 'MediaAgent01'}
            >>> disk_library = DiskLibrary(commcell, 'MyDiskLibrary', library_id='123', library_details=details)

        #ai-gen-doc
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
        self._advanced_library_properties = self._get_advanced_library_properties()
        if library_details is not None:
            self.mountpath = library_details.get('mountPath', None)
            self.mediaagent = library_details.get('mediaAgentName', None)

    def __repr__(self) -> str:
        """Return the string representation of the DiskLibrary instance.

        This method provides a developer-friendly string that represents the current
        DiskLibrary object, which is useful for debugging and logging purposes.

        Returns:
            A string representation of the DiskLibrary instance.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> print(repr(disk_lib))
            <DiskLibrary object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """
        representation_string = 'DiskLibrary class instance for library: "{0}" of Commcell: "{1}"'
        return representation_string.format(
            self.library_name, self._commcell_object.commserv_name
        )

    def move_mountpath(
        self,
        mountpath_id: int,
        source_device_path: str,
        source_mediaagent_id: int,
        target_device_path: str,
        target_mediaagent_id: int,
        target_device_id: int = 0
    ) -> 'Job':
        """Perform the move mountpath operation for a disk library.

        This method moves a mountpath from a source device and media agent to a target device and media agent.
        Optionally, you can specify the target device ID if the target path already exists.

        Args:
            mountpath_id: The ID of the mountpath to be moved.
            source_device_path: The current location of the mountpath.
            source_mediaagent_id: The ID of the MediaAgent where the current mountpath exists.
            target_device_path: The new location for the mountpath.
            target_mediaagent_id: The ID of the MediaAgent where the new mountpath will reside.
            target_device_id: The device ID of the target path if it already exists (default is 0).

        Returns:
            Job: An instance of the Job class representing the move mountpath job.

        Raises:
            Exception: If any argument has an invalid datatype, if the API response error code is not 0,
                if the response is empty, or if the response code is not as expected.

        Example:
            >>> disk_library = DiskLibrary()
            >>> job = disk_library.move_mountpath(
            ...     mountpath_id=1234,
            ...     source_device_path='/old/path',
            ...     source_mediaagent_id=101,
            ...     target_device_path='/new/path',
            ...     target_mediaagent_id=102,
            ...     target_device_id=0
            ... )
            >>> print(f"Move mountpath job started with Job ID: {job.job_id}")

        #ai-gen-doc
        """

        if not (isinstance(mountpath_id, int) and
                isinstance(source_mediaagent_id, int) and
                isinstance(target_mediaagent_id, int) and
                (isinstance(target_device_path, str) or target_device_id > 0) and
                isinstance(source_device_path, str)):
            raise SDKException('Storage', '101')

        MOVE_MOUNTPATH_DETAILS = self._commcell_object._services['GET_MOVE_MOUNTPATH_DETAILS'] % (mountpath_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', MOVE_MOUNTPATH_DETAILS)

        source_device_id = None

        if flag:
            if response.json():
                if 'sourceDeviceInfo' in response.json():
                    source_device_id = response.json().get('sourceDeviceInfo').get('deviceId', None)
                if not source_device_id:
                    raise SDKException('Storage', '102', 'Failed to get details of the mountpath for move')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        request_json = {
            'MPMoveOption': {
                'mountPathMoveList': [{
                    'sourceDeviceId': source_device_id,
                    'sourcemediaAgentId': source_mediaagent_id,
                    'targetMediaAgentId': target_mediaagent_id,
                }]
            }
        }
        if target_device_id > 0:
            request_json['MPMoveOption']['mountPathMoveList'][0]['targetDeviceId'] = target_device_id
        else:
            request_json['MPMoveOption']['mountPathMoveList'][0]['targetDevicePath'] = target_device_path

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['MOVE_MOUNTPATH'], request_json)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    if len(response.json()['jobIds']) == 1:
                        from cvpysdk.job import Job
                        return Job(self._commcell_object, response.json()['jobIds'][0])
                    else:
                        from cvpysdk.job import Job
                        mp_move_job_list = []
                        for job_id in response.json()['jobIds']:
                            mp_move_job_list.append(Job(self._commcell_object, job_id))
                        return mp_move_job_list

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

    def validate_mountpath(self, mountpath_drive_id: int, media_agent: str) -> 'Job':
        """Perform storage validation on a specified mountpath.

        This method initiates a storage validation job for the given mountpath drive ID
        on the specified MediaAgent. It returns a Job instance representing the validation job.

        Args:
            mountpath_drive_id: The drive ID of the mountpath to validate.
            media_agent: The name of the MediaAgent where the mountpath exists.

        Returns:
            Job: An instance of the Job class representing the storage validation job.

        Raises:
            Exception: If the argument data types are invalid.
            Exception: If the API response error code is not 0.
            Exception: If the response is empty.
            Exception: If the response code is not as expected.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> job = disk_lib.validate_mountpath(101, "MediaAgent01")
            >>> print(f"Validation job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        if not (isinstance(mountpath_drive_id, int) and
                isinstance(media_agent, str)):
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

    def add_cloud_mount_path(self, mount_path: str, media_agent: str, username: str, password: str, server_type: int, saved_credential_name: str = "") -> None:
        """Add a cloud mount path to the disk library.

        This method registers a new mount path for a cloud storage container or bucket, 
        associating it with a specified MediaAgent and access credentials.

        Args:
            mount_path: The cloud container or bucket path to be added as a mount path.
            media_agent: The name of the MediaAgent where the mount path will be configured.
            username: The username to access the mount path, in the format <Service Host>//<Account Name>.
                Example: 's3.us-west-1.amazonaws.com//MyAccessKeyID'.
            password: The password or secret key to access the mount path.
            server_type: The integer code representing the cloud library server type.
                Example: 3 for Microsoft Azure Storage.
            saved_credential_name: (Optional) The name of a saved credential to use for authentication. Defaults to an empty string.

        Raises:
            Exception: If any of the following occur:
                - One or more arguments have an invalid data type.
                - The server_type value is incorrect.
                - The API response contains an error code or is empty.
                - The response code is not as expected.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.add_cloud_mount_path(
            ...     mount_path="mybucket",
            ...     media_agent="MediaAgent01",
            ...     username="s3.us-west-1.amazonaws.com//MyAccessKeyID",
            ...     password="MySecretAccessKey",
            ...     server_type=3,
            ...     saved_credential_name="MySavedCredential"
            ... )
            >>> print("Cloud mount path added successfully.")

        #ai-gen-doc
        """

        if not (isinstance(mount_path, str) or isinstance(media_agent, str)
                or isinstance(username, str) or isinstance(password, str)
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
                "serverType": server_type,
                "savedCredential": {
                    "credentialName": saved_credential_name
                }
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

    def add_storage_accelerator_credential(self, mount_path: str, saved_credential: str = "", reset: bool = False) -> None:
        """Add a storage accelerator credential to the specified cloud mount path.

        This method associates a saved credential with a given mount path for storage acceleration.
        Optionally, the credential can be reset if required.

        Args:
            mount_path: The mount path to which the secondary credential should be added.
            saved_credential: The name of the saved credential to associate with the mount path. Defaults to an empty string.
            reset: If True, resets the storage accelerator credential for the mount path. Defaults to False.

        Raises:
            Exception: If the mount_path datatype is invalid.
            Exception: If the API response error code is not 0.
            Exception: If the response is empty.
            Exception: If the response code is not as expected.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.add_storage_accelerator_credential('/mnt/cloud_storage', saved_credential='my_credential')
            >>> # To reset the credential:
            >>> disk_lib.add_storage_accelerator_credential('/mnt/cloud_storage', reset=True)

        #ai-gen-doc
        """

        if not isinstance(mount_path, str):
            raise SDKException('Storage', '101')

        request_json = {
                        "library": {
                            "mediaAgentName": self.media_agent,
                            "libraryName": self._library_name,
                            "mountPath": mount_path,
                            "opType": 8
                        },
                        "libNewProp": {
                            "secondaryCredential": {
                                "credentialName": saved_credential
                            },
                            "resetSecondaryCredentials": reset
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
            _stdout = 'Failed to add storage accelerator credential with error: \n [{0}]'
            _stderr = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', _stdout.format(_stderr))

    def _get_library_properties(self) -> dict:
        """Retrieve the properties of the disk library.

        Returns:
            dict: A dictionary containing the properties of this disk library.

        Raises:
            SDKException: If the response is empty, if the disk library properties could not be retrieved,
                or if the response indicates a failure.

        Example:
            >>> disk_library = DiskLibrary()
            >>> properties = disk_library._get_library_properties()
            >>> print(properties)
            {'libraryName': 'DiskLib1', 'mountPath': '/mnt/storage', ...}

        #ai-gen-doc
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

    def _get_advanced_library_properties(self) -> dict:
        """Retrieve the advanced properties of the disk library.

        Returns:
            dict: A dictionary containing the advanced properties of the disk library.

        Raises:
            SDKException: If the response is empty, if the disk library properties could not be retrieved,
                or if the response indicates a failure.

        Example:
            >>> advanced_props = disk_library._get_advanced_library_properties()
            >>> print(advanced_props)
            {'property1': 'value1', 'property2': 'value2'}
        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', f"{self._library_properties_service}?propertylevel=20"
        )

        if flag:
            if response.json():
                if 'libraryInfo' in response.json():
                    return response.json()['libraryInfo']
                raise SDKException('Storage', '102', 'Failed to get disk Library properties')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)


    def _get_library_id(self) -> str:
        """Retrieve the unique identifier associated with this disk library.

        Returns:
            The library ID as a string.

        Example:
            >>> disk_library = DiskLibrary(commcell_object, "MyDiskLibrary")
            >>> library_id = disk_library._get_library_id()
            >>> print(f"Disk library ID: {library_id}")

        #ai-gen-doc
        """
        libraries = DiskLibraries(self._commcell_object)
        return libraries.get(self.library_name).library_id

    def refresh(self) -> None:
        """Reload the properties of this disk library from the Commcell.

        This method updates the disk library's properties to reflect the latest state 
        as stored in the Commcell. Use this if you suspect the library's configuration 
        has changed outside of the current object instance.

        Example:
            >>> disk_library = DiskLibrary(commcell_object, "MyDiskLibrary")
            >>> disk_library.refresh()
            >>> print("Disk library properties refreshed.")

        #ai-gen-doc
        """
        self._library_properties = self._get_library_properties()
        self._advanced_library_properties = self._get_advanced_library_properties()

    def add_mount_path(self, mount_path: str, media_agent: str, username: str = '', password: str = '') -> None:
        """Add a mount path (local or remote) to the disk library.

        This method registers a new mount path to the disk library, which can be located 
        either locally or remotely on the specified MediaAgent. Optionally, credentials 
        can be provided for accessing the mount path.

        Args:
            mount_path: The path to be added to the disk library. This can be a local or remote path on the MediaAgent.
            media_agent: The name of the MediaAgent where the mount path exists.
            username: (Optional) Username required to access the mount path, if applicable.
            password: (Optional) Password required to access the mount path, if applicable.

        Raises:
            Exception: If the mount_path or media_agent parameters are of invalid type.
            Exception: If the API response error code is not 0.
            Exception: If the response is empty.
            Exception: If the response code is not as expected.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.add_mount_path('/mnt/storage1', 'MediaAgent01')
            >>> # With credentials for a remote mount path
            >>> disk_lib.add_mount_path('\\\\remote-server\\share', 'MediaAgent01', username='user', password='pass')

        #ai-gen-doc
        """

        if not isinstance(mount_path, str) or not isinstance(media_agent, str):
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
    
    def delete_mount_path(self, mount_path: str, media_agent: str, username: str = '', password: str = '') -> None:
        """Delete a mount path from the disk library.

        This method removes an existing mount path from the disk library, which can be located 
        either locally or remotely on the specified MediaAgent. Optionally, credentials can be 
        provided if required for authentication.

        Args:
            mount_path: The path to be deleted from the disk library. This can be a local or remote path on the MediaAgent.
            media_agent: The name of the MediaAgent where the mount path exists.
            username: (Optional) Username required to access the mount path, if applicable.
            password: (Optional) Password required to access the mount path, if applicable.
        Raises:
            SDKException: If the mount_path or media_agent parameters are of invalid type.
            SDKException: If the API response error code is not 0.
            SDKException: If the response is empty.
            SDKException: If the response code is not as expected.
        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.delete_mount_path('/mnt/storage1', 'MediaAgent01')
            >>> # With credentials for a remote mount path
            >>> disk_lib.delete_mount_path('\\\\remote-server\\share', 'MediaAgent01', username='user', password='pass')
        """
        if not isinstance(mount_path, str) or not isinstance(media_agent, str):
            raise SDKException('Storage', '101')

        request_json = {
                    "isConfigRequired": 1,
                    "library": {
                        "opType": 16,
                        "mediaAgentName": media_agent,
                        "libraryName": self._library_name,
                        "mountPath": mount_path,
                        "loginName": username,
                        "password": b64encode(password.encode()).decode(),
                    }
        }

        exec_command = self._commcell_object._services['LIBRARY']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', exec_command, request_json
        )
        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    if response.json()['errorCode'] != 0:
                        raise SDKException('Storage', '102', response.json()['errorMessage'])
        else:
            _stderr = self._commcell_object._update_response_(response.text)
            _stdout = f'Failed to delete mountpath {mount_path} for library {self._library_name} with error: \n {_stderr}'
            raise SDKException('Response', '101', _stdout)
    
    def set_mountpath_reserve_space(self, mount_path: str, size: int) -> None:
        """Set the reserve space on a specified mount path.

        This method configures the amount of disk space (in MB) to reserve on the given mount path
        for the disk library. Reserving space can help prevent the mount path from filling up completely.

        Args:
            mount_path: The file system path to the mount location where reserve space should be set.
            size: The amount of space to reserve on the mount path, in megabytes (MB).

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.set_mountpath_reserve_space('/mnt/storage1', 10240)
            >>> print("Reserve space of 10 GB set on /mnt/storage1")

        #ai-gen-doc
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

    def set_max_data_to_write_on_mount_path(self, mount_path: str, size: int) -> None:
        """Set the maximum amount of data that can be written to a specific mount path.

        This method configures a limit on the total data (in megabytes) that can be written to the specified mount path
        within the disk library.

        Args:
            mount_path: The folder path representing the mount path to configure.
            size: The maximum data (in megabytes) allowed to be written to the mount path.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.set_max_data_to_write_on_mount_path('/mnt/storage1', 50000)
            >>> # The mount path '/mnt/storage1' will now have a 50 GB write limit

        #ai-gen-doc
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
                      "maxDataToWriteMB": size
                    }
                }
        }
        self._commcell_object.qoperation_execute(request_json)

    def change_device_access_type(
        self,
        mountpath_id: int,
        device_id: int,
        device_controller_id: int,
        media_agent_id: int,
        device_access_type: int
    ) -> None:
        """Change the access type for a specific device in the disk library.

        This method updates the access type for a device associated with a given mount path, device controller, 
        and media agent. The access type determines how the device can be accessed (e.g., read, read/write, preferred)
        and varies depending on the connection type (Regular, IP, Fibre Channel, iSCSI).

        Args:
            mountpath_id: The ID of the mount path associated with the device.
            device_id: The unique identifier of the device.
            device_controller_id: The ID of the device controller managing the device.
            media_agent_id: The ID of the media agent associated with the device.
            device_access_type: The access type value to set for the device. Valid values depend on the connection type:
                - Regular:
                    - Read: 4
                    - Read and Write: 6
                    - Preferred: 8
                - IP:
                    - Read: 20
                    - Read and Write: 22
                - Fibre Channel (FC):
                    - Read: 36
                    - Read and Write: 38
                - iSCSI:
                    - Read: 132
                    - Read and Write: 134

        Example:
            >>> disk_lib = DiskLibrary()
            >>> # Set device access type to 'Read and Write' for a Regular device
            >>> disk_lib.change_device_access_type(
            ...     mountpath_id=101,
            ...     device_id=202,
            ...     device_controller_id=303,
            ...     media_agent_id=404,
            ...     device_access_type=6
            ... )
            >>> print("Device access type updated successfully.")

        #ai-gen-doc
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

    def modify_cloud_access_type(self, mountpath_id: int, device_controller_id: int, device_access_type: int, enabled: bool = True) -> None:
        """Modify the device access type for a cloud mount path.

        This method updates the access type for a specified cloud mount path and device controller.
        The access type determines the allowed operations (read, read/write) for the mount path.

        Args:
            mountpath_id: The ID of the mount path to modify.
            device_controller_id: The ID of the device controller associated with the mount path.
            device_access_type: The desired device access type.
                Possible values:
                    4 - Read
                    6 - Read and Write
                By default, preferred access (value 8) will be set if not specified.
            enabled: Whether to enable the specified access type. Defaults to True.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> # Set mount path to read-only access
            >>> disk_lib.modify_cloud_access_type(101, 5, 4)
            >>> # Set mount path to read and write access, and disable it
            >>> disk_lib.modify_cloud_access_type(101, 5, 6, enabled=False)

        #ai-gen-doc
        """

        if not all([isinstance(mountpath_id, int), isinstance(device_controller_id, int),
                    isinstance(device_access_type, int)]):
            raise SDKException('Storage', '101')

        access = ""
        if device_access_type == 4:
            access = "READ"
        else:
            access = "READ_AND_WRITE"

        payload = {
            "access": access,
            "enable": enabled
        }

        EDIT_CLOUD_CONTROLLER = self._commcell_object._services['EDIT_CLOUD_CONTROLLER'] % (mountpath_id, device_controller_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', EDIT_CLOUD_CONTROLLER, payload)

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json().get('errorCode'))
                    if error_code != 0:
                        error_message = response.json().get('errorMessage')
                        raise SDKException('Storage', '102', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            _stdout = 'Failed to modify cloud access type with error: \n [{0}]'
            _stderr = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', _stdout.format(_stderr))


    def update_device_controller(
        self,
        mountpath_id: int,
        device_id: int,
        device_controller_id: int,
        media_agent_id: int,
        device_access_type: int,
        **kwargs: Any
    ) -> None:
        """Update the properties of a device controller associated with a disk library.

        This method allows you to modify the configuration of a device controller, such as access type,
        credentials, and path information, for a specific mount path and device.

        Args:
            mountpath_id: The ID of the mount path to update.
            device_id: The ID of the device associated with the controller.
            device_controller_id: The ID of the device controller to update.
            media_agent_id: The ID of the media agent managing the device.
            device_access_type: The access type for the device. Supported values:
                - Regular:
                    - Read: 4
                    - Read and Write: 6
                    - Preferred: 8
                - IP:
                    - Read: 20
                    - Read/Write: 22
                - Fibre Channel (FC):
                    - Read: 36
                    - Read and Write: 38
                - iSCSI:
                    - Read: 132
                    - Read and Write: 134
            **kwargs: Optional keyword arguments for additional configuration.
                - username (str): Username for the device. For cloud libraries, use the format <vendorURL>//__CVCRED__.
                - password (str): Password for the device. Use a dummy password if credential_name is provided.
                - credential_name (str): Credential name as stored in the credential manager.
                - path (str): Access path for the media agent (local or UNC).

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.update_device_controller(
            ...     mountpath_id=101,
            ...     device_id=202,
            ...     device_controller_id=303,
            ...     media_agent_id=404,
            ...     device_access_type=6,
            ...     username="admin",
            ...     password="password123",
            ...     path="\\\\server\\share"
            ... )
            >>> print("Device controller updated successfully")

        #ai-gen-doc
        """

        if not all([isinstance(mountpath_id, int), isinstance(device_id, int), isinstance(device_controller_id, int),
                    isinstance(media_agent_id, int), isinstance(device_access_type, int)]):
            raise SDKException('Storage', '101')

        username = kwargs.get("username", "")
        password = kwargs.get("password", "")
        credential_name = kwargs.get("credential_name", "")
        path = kwargs.get("path", self.mount_path)
        enabled = 1
        if not kwargs.get('enabled', True):
            enabled = 0
        request_json = {
            "EVGui_MMDevicePathInfoReq":
                {
                    "mountpathId": mountpath_id,
                    "infoList": {
                        "password": password,
                        "accessType": device_access_type,
                        "deviceId": device_id,
                        "deviceControllerId": device_controller_id,
                        "path": path,
                        "enabled": enabled,
                        "numWriters": -1,
                        "opType": 2,
                        "autoPickTransportType": 0,
                        "protocolType": 679,
                        "mediaAgent": {
                            "id": media_agent_id
                        },
                        "savedCredential": {
                            "credentialName": credential_name
                        },
                        "userName": username
                    }
                }
        }

        self._commcell_object.qoperation_execute(request_json)


    def verify_media(self, media_name: str, location_id: int) -> None:
        """Perform a verify media operation on a specified media in the disk library.

        Args:
            media_name: The barcode of the media to verify.
            location_id: The slot ID of the media within the library.

        Example:
            >>> disk_library = DiskLibrary()
            >>> disk_library.verify_media(media_name="ABC123", location_id=42)
            >>> print("Media verification initiated for slot 42 with barcode ABC123")

        #ai-gen-doc
        """

        if not (isinstance(media_name, str) and
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
    def free_space(self) -> str:
        """Get the available free space in the disk library.

        Returns:
            The amount of free space available, in bytes.

        Example:
            >>> disk_library = DiskLibrary()
            >>> available_space = disk_library.free_space  # Use dot notation for property
            >>> print(f"Free space: {available_space} bytes")

        #ai-gen-doc
        """
        return self._library_properties.get('magLibSummary', {}).get('totalFreeSpace').strip()

    @property
    def mountpath_usage(self) -> Dict[str, Any]:
        """Get the usage statistics for all mount paths in the disk library.

        Returns:
            Dictionary containing usage information for each mount path. The keys are mount path identifiers,
            and the values provide details such as total space, used space, and free space.

        Example:
            >>> disk_library = DiskLibrary()
            >>> usage_info = disk_library.mountpath_usage
            >>> for mount_path, stats in usage_info.items():
            ...     print(f"Mount Path: {mount_path}, Used: {stats['used_space']} GB, Free: {stats['free_space']} GB")

        #ai-gen-doc
        """
        return self._library_properties.get('magLibSummary', {}).get('mountPathUsage').strip()

    @mountpath_usage.setter
    def mountpath_usage(self, value: str) -> None:
        """Set the mount path usage option for the disk library.

        Args:
            value: The mount path usage mode to set. Must be either 'SPILL_AND_FILL' or 'FILL_AND_SPILL'.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.mountpath_usage = 'SPILL_AND_FILL'  # Use assignment for property setter
            >>> # The mount path usage is now set to 'SPILL_AND_FILL'

        #ai-gen-doc
        """
        if not isinstance(value, str):
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

    def set_mountpath_preferred_on_mediaagent(self, value: bool) -> None:
        """Set the 'prefer mount path according to media agent' option on the disk library.

        This method configures whether the disk library should select the preferred mount path
        based on the associated media agent setting.

        Args:
            value: If True, the library will prefer mount paths according to the media agent.
                   If False, this preference is disabled.

        Raises:
            SDKException: If the update fails or if the input value is not a boolean.

        Example:
            >>> disk_library = DiskLibrary()
            >>> disk_library.set_mountpath_preferred_on_mediaagent(True)
            >>> # The disk library is now set to prefer mount paths according to the media agent

        #ai-gen-doc
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
    def media_agents_associated(self) -> List[str]:
        """Get the list of media agents associated with the disk library.

        Returns:
            List of media agent names (as strings) that are currently associated with this disk library.

        Example:
            >>> disk_library = DiskLibrary()
            >>> media_agents = disk_library.media_agents_associated
            >>> print("Associated media agents:", media_agents)
            >>> # Output might be: Associated media agents: ['MediaAgent1', 'MediaAgent2']

        #ai-gen-doc
        """
        mount_paths = self._library_properties.get('MountPathList')
        media_agents = [mount_path.get('mountPathName').split('[')[1].split(']')[0] for mount_path in mount_paths if "mountPathName" in mount_path]
        return list(set(media_agents))

    @property
    def name(self) -> str:
        """Get the display name of the disk library.

        Returns:
            The display name of the disk library as a string.

        Example:
            >>> disk_library = DiskLibrary()
            >>> library_name = disk_library.name  # Use dot notation for property access
            >>> print(f"Disk library name: {library_name}")

        #ai-gen-doc
        """
        return self._library_properties['MountPathList'][0]['mountPathSummary']['libraryName']

    @property
    def library_name(self) -> str:
        """Get the name of the disk library as a read-only property.

        Returns:
            The name of the disk library.

        Example:
            >>> disk_library = DiskLibrary()
            >>> name = disk_library.library_name  # Access the library name property
            >>> print(f"Library name: {name}")
        #ai-gen-doc
        """
        return self._library_name

    @property
    def library_id(self) -> str:
        """Get the unique identifier of the disk library as a read-only property.

        Returns:
            The library ID as a string.

        Example:
            >>> disk_library = DiskLibrary(commcell_object, "MyDiskLibrary")
            >>> lib_id = disk_library.library_id  # Access the library ID property
            >>> print(f"Disk Library ID: {lib_id}")

        #ai-gen-doc
        """
        return self._library_id

    @property
    def library_properties(self) -> dict:
        """Get the full set of properties for the disk library as a dictionary.

        Returns:
            dict: A dictionary containing all properties and configuration details of the disk library.

        Example:
            >>> disk_lib = DiskLibrary(commcell_object, 'MyDiskLibrary')
            >>> properties = disk_lib.library_properties
            >>> print(properties)
            >>> # Access specific property
            >>> print(properties.get('libraryName'))

        #ai-gen-doc
        """
        self.refresh()
        return self._library_properties

    @property
    def advanced_library_properties(self) -> Dict[str, Any]:
        """Get the advanced properties of the disk library.

        Returns:
            Dictionary containing advanced properties and configuration details of the disk library.

        Example:
            >>> disk_lib = DiskLibrary(commcell_object, "LibraryName")
            >>> advanced_props = disk_lib.advanced_library_properties  # Use dot notation for property
            >>> print("Advanced properties:", advanced_props)
            >>> # Access specific property
            >>> cache_size = advanced_props.get("CacheSize")
            >>> print(f"Cache size: {cache_size}")

        #ai-gen-doc
        """
        self.refresh()
        return self._advanced_library_properties

    @property
    def mount_path(self) -> str:
        """Get the mount path associated with this disk library.

        Returns:
            The mount path of the disk library as a string.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> path = disk_lib.mount_path  # Use dot notation for property access
            >>> print(f"Disk library mount path: {path}")

        #ai-gen-doc
        """
        return self.mountpath

    @mount_path.setter
    def mount_path(self, mount_path: str) -> None:
        """Set the mount path for the disk library.

        Args:
            mount_path: The file system path to be set as the mount path for the disk library.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.mount_path = "/mnt/storage/disklib"  # Use assignment for property setter
            >>> # The mount path is now set to "/mnt/storage/disklib"

        #ai-gen-doc
        """
        self.mountpath = mount_path

    @property
    def media_agent(self) -> str:
        """Get the name of the media agent associated with this disk library.

        Returns:
            The name of the media agent as a string.

        Example:
            >>> disk_library = DiskLibrary()
            >>> agent_name = disk_library.media_agent  # Access the media agent property
            >>> print(f"Media agent: {agent_name}")
        #ai-gen-doc
        """
        return self.mediaagent

    @media_agent.setter
    def media_agent(self, media_agent: str) -> None:
        """Set the media agent associated with this DiskLibrary.

        Args:
            media_agent: The name of the media agent to assign to the DiskLibrary.

        Example:
            >>> disk_library = DiskLibrary()
            >>> disk_library.media_agent = "MediaAgent01"  # Use assignment for property setter
            >>> # The DiskLibrary is now associated with 'MediaAgent01'

        #ai-gen-doc
        """
        self.mediaagent = media_agent

    def share_mount_path(self, new_media_agent: str, new_mount_path: str, **kwargs: Any) -> None:
        """Share a mount path with a specified media agent.

        This method allows you to share an existing mount path with another media agent, 
        optionally specifying additional parameters such as access type, credentials, and 
        library details via keyword arguments.

        Args:
            new_media_agent: The name of the media agent that will access the shared mount path.
            new_mount_path: The identifier of the mount path to be shared.
            **kwargs: Optional keyword arguments to customize the sharing operation. Supported options include:
                - media_agent (str): Media agent associated with the library.
                - library_name (str): Name of the library containing the mount path.
                - mount_path (str): The mount path to be shared.
                - access_type (int): Access type for the shared mount path. Possible values:
                    * 4   - Read Device Access
                    * 6   - Read/Write Device Access
                    * 12  - Read Device Access with Preferred
                    * 14  - Read/Write Device Access with Preferred
                    * 20  - Data Server - IP Read
                    * 22  - Data Server - IP Read/Write
                    * 36  - Data Server - FC Read
                    * 38  - Data Server - FC Read/Write
                    * 132 - Data Server - iSCSI Read
                    * 134 - Data Server - iSCSI Read/Write
                    Note: For Data Server device access types, provide the local path in both the 
                    library/mountPath and libNewProp/mountPath parameters.
                - username (str): Username for accessing the mount path (if UNC).
                - password (str): Password for accessing the mount path (if UNC).
                - credential_name (str): Credential name for the credential manager. For cloud libraries, 
                  update the username parameter in the format "<vendorURL>//__CVCRED__" (e.g., 
                  "s3.amazonaws.com//__CVCRED__") and provide a dummy value for the password.

        Raises:
            Exception: If any parameter has an invalid datatype, if the API response error code is not 0,
                if the response is empty, or if the response code is not as expected.

        Example:
            >>> disk_lib = DiskLibrary()
            >>> disk_lib.share_mount_path(
            ...     new_media_agent="MediaAgent02",
            ...     new_mount_path=12345,
            ...     access_type=6,
            ...     username="user",
            ...     password="pass"
            ... )
            >>> print("Mount path shared successfully.")

        #ai-gen-doc
        """

        media_agent = kwargs.get('media_agent', self.mediaagent)
        library_name = kwargs.get('library_name', self.library_name)
        mount_path = kwargs.get('mount_path', self.mountpath)
        access_type = kwargs.get('access_type', 22)
        username = kwargs.get('username', '')
        password = kwargs.get('password', '')
        credential_name = kwargs.get('credential_name', '')

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
            "proxyPassword": "",
            "savedCredential": {
                "credentialName": credential_name
            }
        }
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

    def delete_media_agent_on_mount_path(self, device_id, media_agent_name, device_controller_id, mountPathId):
        """
        Method to delete media agent on mount path

        Args:

            device_id (int)         -- Device id

            media_agent_name (str)  -- Media agent which is accessing the shared mount path

            device_controller_id (int) -- Device controller id

            mountPathId (int)       -- Mount path id of the mount path

        """

        request_json = {"infoList": [
                {"deviceId": device_id,
                 "deviceControllerId": device_controller_id,
                 "mediaAgent": {"name": media_agent_name},
                 "enabled": 1,
                 "opType": 3,
                 "accessible": True}
            ],
            "mountpathId": mountPathId
            }

        DELETE_DEVICE_CONTROLLER = self._commcell_object._services['DELETE_DEVICE_CONTROLLER']
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', DELETE_DEVICE_CONTROLLER, request_json)

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json().get('errorCode'))
                    if error_code != 0:
                        error_message = response.json().get('errorMessage')
                        raise SDKException('Storage', '102', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            _stdout = 'Failed to delete media agent on mount path with error: \n [{0}]'
            _stderr = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', _stdout.format(_stderr))

class RPStores(object):
    """
    Manages RP (Recovery Point) Stores within a Commcell environment.

    This class provides an interface for interacting with RP Stores, allowing users to
    add new stores, check for the existence of specific stores, retrieve store details,
    and refresh the internal store list. It is designed to facilitate efficient management
    and access to RP Stores, which are essential for data recovery operations.

    Key Features:
        - Initialization with a Commcell object for context
        - Retrieval of all RP Stores
        - Addition of new RP Stores with specified parameters
        - Existence check for a given RP Store by name
        - Access to details of a specific RP Store
        - Refreshing the RP Store list to ensure up-to-date information

    #ai-gen-doc
    """
    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize an instance of the RPStores class.

        Args:
            commcell: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> rpstores = RPStores(commcell)
            >>> print("RPStores object created successfully")

        #ai-gen-doc
        """
        self._commcell = commcell
        self._rp_stores = None
        self.refresh()

    def _get_rp_stores(self) -> dict:
        """Retrieve the list of Recovery Point (RP) stores associated with this object.

        Returns:
            Dict: A dictionary containing information about each RP store.

        Example:
            >>> rp_stores = rpstores_obj._get_rp_stores()
            >>> print(f"Number of RP stores: {len(rp_stores)}")
            >>> # Each item in the list represents an RP store's details

        #ai-gen-doc
        """
        flag, response = self._commcell._cvpysdk_object.make_request('GET', self._commcell._services['ALL_RPStores'])

        try:
            if response.json().get('libraryList'):
                return {library["library"]["libraryName"].lower(): library["MountPathList"][0]["rpStoreLibraryInfo"]
                        ["rpStoreId"] for library in response.json()["libraryList"]}
            return {}
        except (KeyError, ValueError):
            generic_msg = "Unable to fetch RPStore"
            err_msg = response.json().get("errorMessage", generic_msg) if response.status_code == 200 else generic_msg
            raise SDKException('Storage', '102', '{0}'.format(err_msg))

    def add(self, name: str, path: str, storage: int, media_agent_name: str) -> 'RPStore':
        """Add a new RPStore with the specified configuration.

        Args:
            name: The name to assign to the new RPStore.
            path: The file system path where the RPStore will be created.
            storage: The storage capacity of the RPStore in gigabytes (GB).
            media_agent_name: The name of the media agent to associate with the RPStore.

        Returns:
            RPStore: An instance representing the newly created RPStore.

        Example:
            >>> rpstores = RPStores()
            >>> rpstore = rpstores.add(
            ...     name="MyRPStore",
            ...     path="/mnt/rpstore",
            ...     storage=500,
            ...     media_agent_name="MediaAgent01"
            ... )
            >>> print(f"RPStore created: {rpstore}")

        #ai-gen-doc
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

    def has_rp_store(self, rpstore_name: str) -> bool:
        """Check if a specific RPStore exists in the current RPStores collection.

        Args:
            rpstore_name: The name of the RPStore to check for existence.

        Returns:
            True if the specified RPStore is present, otherwise False.

        Example:
            >>> rpstores = RPStores()
            >>> exists = rpstores.has_rp_store("MyRPStore")
            >>> print(f"RPStore exists: {exists}")
            # Output: RPStore exists: True

        #ai-gen-doc
        """
        if not isinstance(rpstore_name, str):
            raise SDKException('Storage', '101')

        return rpstore_name.lower() in self._rp_stores

    def get(self, rpstore_name: str) -> 'RPStore':
        """Retrieve an instance of the specified RPStore by name.

        Args:
            rpstore_name: The name of the RPStore to fetch.

        Returns:
            RPStore: An instance representing the requested RPStore.

        Example:
            >>> rpstores = RPStores()
            >>> rpstore = rpstores.get("MyRPStore")
            >>> print(f"Fetched RPStore: {rpstore}")

        #ai-gen-doc
        """
        if not isinstance(rpstore_name, str):
            raise SDKException('Storage', '101')

        try:
            return RPStore(self._commcell, rpstore_name, self._rp_stores[rpstore_name.lower()])
        except KeyError:
            raise SDKException('Storage', '102', 'No RPStore exists with name: {0}'.format(rpstore_name))

    def refresh(self) -> None:
        """Reload the media agent information associated with the Commcell.

        This method clears any cached data about media agents, ensuring that subsequent accesses
        retrieve the most up-to-date information from the Commcell.

        Example:
            >>> rpstores = RPStores(commcell_object)
            >>> rpstores.refresh()  # Refresh the list of media agents
            >>> print("Media agent information refreshed.")

        #ai-gen-doc
        """
        self._rp_stores = self._get_rp_stores()


class RPStore(object):
    """
    Represents a Recovery Point Store (RPStore) within a CommCell environment.

    This class encapsulates the properties and identification details of an RPStore,
    providing access to its name and unique identifier. It is initialized with a
    reference to the associated CommCell, the RPStore's name, and its ID.

    Key Features:
        - Initialization with CommCell context, RPStore name, and ID
        - Access to RPStore name via property
        - Access to RPStore unique identifier via property

    #ai-gen-doc
    """
    def __init__(self, commcell: 'Commcell', rpstore_name: str, rpstore_id: int) -> None:
        """Initialize an instance of the RPStore class.

        Args:
            commcell: The Commcell object representing the connection to the Commcell environment.
            rpstore_name: The name of the RPStore.
            rpstore_id: The unique identifier for the RPStore.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> rpstore = RPStore(commcell, 'MyRPStore', 101)
            >>> print(f"RPStore '{rpstore_name}' with ID {rpstore_id} initialized successfully.")

        #ai-gen-doc
        """
        self._commcell = commcell
        self._rpstore_name = rpstore_name.lower()
        self._rpstore_id = rpstore_id

    @property
    def rpstore_name(self) -> str:
        """Get the name of the RPStore.

        Returns:
            The name of the RPStore as a string.

        Example:
            >>> rpstore = RPStore()
            >>> name = rpstore.rpstore_name  # Access the RPStore name using the property
            >>> print(f"RPStore name: {name}")

        #ai-gen-doc
        """
        return self._rpstore_name

    @property
    def rpstore_id(self) -> int:
        """Get the unique identifier (ID) of the RPStore.

        Returns:
            int: The unique RPStore ID.

        Example:
            >>> rpstore = RPStore()
            >>> store_id = rpstore.rpstore_id  # Access the RPStore ID using the property
            >>> print(f"RPStore ID: {store_id}")

        #ai-gen-doc
        """
        return self._rpstore_id



class TapeLibraries(Libraries):
    """
    Manages tape library operations within the context of a CommCell environment.

    The TapeLibraries class provides a comprehensive interface for interacting with tape libraries,
    including detection, configuration, locking/unlocking of media management configurations, and
    management of individual tape libraries. It is designed to facilitate administration and automation
    of tape library resources, leveraging underlying CommCell objects and media agents.

    Key Features:
        - Initialization with a CommCell object for context-aware operations
        - String representation for easy identification and debugging
        - Retrieval of tape library details by name
        - Deletion of tape libraries by name
        - Locking and unlocking of media management configurations, with support for forced locking
        - Detection of tape libraries across specified media agents
        - Configuration of tape libraries with specified media agents

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a TapeLibraries object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> tape_libraries = TapeLibraries(commcell)
            >>> print("TapeLibraries object created successfully")

        #ai-gen-doc
        """
        super().__init__(commcell_object)
        self._commcell_object = commcell_object
        self._DETECT_TAPE_LIBRARY = self._commcell_object._services['DETECT_TAPE_LIBRARY']
        self._CONFIGURE_TAPE_LIBRARY = self._commcell_object._services['CONFIGURE_TAPE_LIBRARY']
        self._LOCK_MM_CONFIGURATION = self._commcell_object._services['LOCK_MM_CONFIGURATION']


    def __str__(self) -> str:
        """Return a string representation of all tape libraries associated with the Commcell.

        This method provides a human-readable summary of all tape libraries managed by the TapeLibraries object.

        Returns:
            A string listing all tape libraries associated with the Commcell.

        Example:
            >>> tape_libraries = TapeLibraries(commcell_object)
            >>> print(str(tape_libraries))
            TapeLibrary1, TapeLibrary2, TapeLibrary3

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Tape Library')

        for index, library in enumerate(self._libraries):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, library)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the TapeLibraries instance.

        This method provides a developer-friendly string that represents the TapeLibraries object,
        typically used for debugging and logging purposes.

        Returns:
            A string representation of the TapeLibraries instance.

        Example:
            >>> tape_libraries = TapeLibraries(commcell_object)
            >>> print(repr(tape_libraries))
            <TapeLibraries object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """
        return "TapeLibraries class instance for Commcell"



    def get(self, tape_library_name: str) -> 'TapeLibrary':
        """Retrieve the TapeLibrary object for the specified library name.

        Args:
            tape_library_name: The name of the tape library to retrieve.

        Returns:
            TapeLibrary: An object representing the specified tape library.

        Raises:
            SDKException: If the type of the library name argument is not a string.

        Example:
            >>> tape_libraries = TapeLibraries(commcell_object)
            >>> library = tape_libraries.get("Library1")
            >>> print(f"Retrieved tape library: {library}")

        #ai-gen-doc
        """

        if not isinstance(tape_library_name, str):
            raise SDKException('Storage', '101')
        else:
            if self.has_library(tape_library_name):
                tape_library_name = tape_library_name.lower()
                return TapeLibrary(self._commcell_object, tape_library_name, self._libraries[tape_library_name])

    def delete(self, tape_library_name: str) -> None:
        """Delete the specified tape library by name.

        Args:
            tape_library_name: The name of the tape library to delete.
            
        Raises:
            SDKException: If the tape_library_name is not a string, if the library does not exist,
                or if the deletion fails.

        Example:
            >>> tape_libraries = TapeLibraries(commcell_object)
            >>> result = tape_libraries.delete("Library1")
            >>> print(f"Library deleted: {result}")

        #ai-gen-doc
        """

        if not isinstance(tape_library_name, str):
            raise SDKException('Storage', '101')

        if not self.has_library(tape_library_name):
            raise SDKException('Storage', '101', "Invalid library name")

        pay_load={
                "isDeconfigLibrary": 1,
                "library": {
                    "opType": 2,
                    "libraryName": tape_library_name
                }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._LIBRARY, pay_load)

        if not flag:
            raise SDKException('Storage', '102', "Failed to DELETE the library")

        self.refresh()


    def __lock_unlock_mm_configuration(self, operation: int) -> None:
        """Lock or unlock the MM (Media Management) configuration for tape library detection.

        This method performs a lock, unlock, or force lock operation on the MM configuration,
        which is required for certain tape library management tasks.

        Args:
            operation: The operation type to perform.
                1 - Lock the MM configuration.
                0 - Unlock the MM configuration.
                2 - Force lock the MM configuration.

        Raises:
            SDKException: If the API call is unsuccessful, the response is invalid,
                the errorCode is missing from the response JSON, or the lock/unlock operation fails.

        Example:
            >>> tape_libraries = TapeLibraries(commcell_object)
            >>> tape_libraries._TapeLibraries__lock_unlock_mm_configuration(1)  # Lock MM configuration
            >>> tape_libraries._TapeLibraries__lock_unlock_mm_configuration(0)  # Unlock MM configuration
            >>> tape_libraries._TapeLibraries__lock_unlock_mm_configuration(2)  # Force lock MM configuration

        #ai-gen-doc
        """

        if not isinstance(operation, int):
            raise SDKException('Storage', '101', "Invalid Operation data type. Expected is integer")

        if not operation in [0,1,2]:
            raise SDKException('Storage', '101', "Invalid Operation type. Expected among [0,1,2] but received "+str(operation))

        pay_load ={
        "configLockUnlock": {
        "lockType": operation
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._LOCK_MM_CONFIGURATION, pay_load)

        if flag :
            if response and response.json():
                if 'errorCode' in response.json():
                    if response.json()['errorCode'] != 0:
                        raise SDKException('Storage', '102', "Failed to lock the MM Config. errorMessage : "+response.json().get('errorMessage'))
                else:
                    raise SDKException('Storage', '102',
                                       "lock_unlock_mm_configuration :: Error code is not part of response JSON")
            else:
                raise SDKException('Response', '102', "Invalid response")
        else:
            raise SDKException('Response', '101', "API call is not successful")

    def lock_mm_configuration(self, forceLock: bool = False) -> None:
        """Lock the Media Management (MM) configuration for tape library detection.

        This method locks the MM configuration to prevent concurrent modifications during
        tape library detection. Optionally, the lock can be forced if required.

        Args:
            forceLock: If True, forces the lock even if another process holds it. Defaults to False.

        Example:
            >>> tape_libraries = TapeLibraries()
            >>> tape_libraries.lock_mm_configuration()  # Lock MM config normally
            >>> tape_libraries.lock_mm_configuration(forceLock=True)  # Force lock MM config

        #ai-gen-doc
        """
        if forceLock:
            self.__lock_unlock_mm_configuration(2)
            return
        self.__lock_unlock_mm_configuration(1)

    def unlock_mm_configuration(self) -> None:
        """Unlock the Media Management (MM) configuration to enable tape library detection.

        This method is used to unlock the MM configuration, allowing the system to detect and configure tape libraries.

        Example:
            >>> tape_libraries = TapeLibraries()
            >>> tape_libraries.unlock_mm_configuration()
            >>> print("MM configuration unlocked for tape library detection.")

        #ai-gen-doc
        """
        self.__lock_unlock_mm_configuration(0)


    def detect_tape_library(self, mediaagents: list) -> dict:
        """Detect tape libraries associated with the specified MediaAgent(s).

        Args:
            mediaagents: A list of MediaAgent names or identifiers for which to detect tape libraries.

        Returns:
            dict: A JSON dictionary containing the response of the tape library detection operation.

        Raises:
            SDKException: If the detection process fails.

        Example:
            >>> tape_libraries = TapeLibraries()
            >>> mediaagents = ['MediaAgent1', 'MediaAgent2']
            >>> response = tape_libraries.detect_tape_library(mediaagents)
            >>> print(response)
            # Output will be a dictionary with detection results for each MediaAgent

        #ai-gen-doc
        """

        pay_load ={
        "autoDetect": True,
        "mediaAgentIdList": mediaagents
        }

        try:
            self.lock_mm_configuration()
            flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._DETECT_TAPE_LIBRARY, pay_load )
        finally:
            self.unlock_mm_configuration()

        if flag and response.json():
            return response.json()
        raise SDKException('Storage', '102', "Failed to detect library")

    def configure_tape_library(self, tape_library_name: str, mediaagents: list) -> 'TapeLibrary':
        """Configure a new tape library with the specified name and associated MediaAgents.

        Args:
            tape_library_name: The name of the tape library to configure.
            mediaagents: List of MediaAgent objects or names to associate with the tape library.

        Returns:
            TapeLibrary: An object representing the configured tape library.

        Raises:
            SDKException: If the tape library configuration fails.

        Example:
            >>> tape_libraries = TapeLibraries(commcell_object)
            >>> library = tape_libraries.configure_tape_library("Library1", ["MediaAgent1", "MediaAgent2"])
            >>> print(f"Configured tape library: {library}")

        #ai-gen-doc
        """

        libraries=self.detect_tape_library(mediaagents)
        flag=False
        for lib in libraries['libraries']:

            if lib['libraryName'] == tape_library_name:
                drive_list=lib['drives']

                pay_load= {
                    "driveList": drive_list,
                    "hdr": {
                        "tag": 0
                    }
                }
                flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._CONFIGURE_TAPE_LIBRARY,
                                                                                    pay_load)
                break

        if not flag:
            raise SDKException('Storage', '102', "Failed to configure the library")

        self.refresh()

        tape_library_name = tape_library_name.lower()
        for lib_name, lib_id in self._libraries.items():
            if lib_name.startswith(tape_library_name + " "):
                return self.get(lib_name)



class TapeLibrary(object):
    """
    Represents a tape library within a CommCell environment.

    This class provides an interface for managing and interacting with tape libraries,
    including retrieving library properties, accessing drive lists, and refreshing
    library information. It encapsulates essential attributes such as the library name
    and ID, and offers utility methods for representation and internal property access.

    Key Features:
        - Initialization with CommCell object, library name, and library ID
        - Access to tape library name and ID via properties
        - Retrieve the list of drives associated with the tape library
        - Fetch and refresh tape library properties
        - String and representation methods for easy identification
        - Internal methods for accessing library ID and properties

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', tape_library_name: str, tape_library_id: int = None) -> None:
        """Initialize a TapeLibrary object representing a specific tape library.

        Args:
            commcell_object: Instance of the Commcell class used to interact with the Commcell environment.
            tape_library_name: The name of the tape library to manage.
            tape_library_id: Optional; the unique identifier for the tape library. If not provided, it may be determined automatically.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> tape_library = TapeLibrary(commcell, 'Library1')
            >>> # Optionally, specify the tape library ID
            >>> tape_library_with_id = TapeLibrary(commcell, 'Library1', tape_library_id=123)

        #ai-gen-doc
        """

        self._commcell_object = commcell_object
        self._services = self._commcell_object._services
        self._name = tape_library_name
        if tape_library_id:
            self._library_id = str(tape_library_id)
        else:
            self._library_id = self._get_library_id()

        self._library_properties_service = self._commcell_object._services[
                                               'GET_LIBRARY_PROPERTIES'] % (self._library_id)

        self.library_properties = self._get_library_properties()

        self._name = self.library_properties['library']['libraryName']

        self.media_details = None
        self.latest_media_details = False


    def __str__(self) -> str:
        """Return a string representation of the tape library.

        This method provides a human-readable summary of the tape library associated with the Commcell.

        Returns:
            A string describing the tape library.

        Example:
            >>> tape_library = TapeLibrary(commcell_object)
            >>> print(str(tape_library))
            Tape Library: <library details here>

        #ai-gen-doc
        """
        representation_string = "TapeLibrary instance of library : {0}"

        return representation_string.format(self._name)

    def __repr__(self) -> str:
        """Return the string representation of the TapeLibrary instance.

        This method provides a developer-friendly string that represents the TapeLibrary object,
        which can be useful for debugging and logging purposes.

        Returns:
            A string describing the TapeLibrary instance.

        Example:
            >>> library = TapeLibrary()
            >>> print(repr(library))
            <TapeLibrary object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """
        representation_string = 'TapeLibrary class instance for library: "{0}" of Commcell: "{1}"'
        return representation_string.format(
            self._name, self._commcell_object.commserv_name
        )


    def _get_library_id(self) -> str:
        """Retrieve the unique identifier associated with this tape library.

        Returns:
            The library ID as a string.

        Example:
            >>> tape_library = TapeLibrary()
            >>> library_id = tape_library._get_library_id()
            >>> print(f"Tape library ID: {library_id}")

        #ai-gen-doc
        """
        libraries = TapeLibraries(self._commcell_object)
        return libraries.get(self.library_name).library_id


    def get_drive_list(self) -> list[list]:
        """Retrieve the list of tape drives associated with this tape library.

        Returns:
            list: A 2D list containing the drives present in this tape library.

        Example:
            >>> tape_library = TapeLibrary()
            >>> drives = tape_library.get_drive_list()
            >>> print(f"Number of drives: {len(drives)}")
            >>> for drive in drives:
            >>>     print(f"Drive: {drive}")

        #ai-gen-doc
        """

        self.refresh()

        drive_list=[]

        if 'DriveList' in self.library_properties:
            for drive in self.library_properties["DriveList"]:
                drive_list.append([drive["driveName"], drive["driveId"]])

        return drive_list


    def _get_library_properties(self) -> Dict[str, Any]:
        """Retrieve the properties of the tape library.

        Returns:
            Dictionary containing the properties of the tape library.

        Raises:
            SDKException: If the response is empty, if the tape library properties could not be retrieved,
                or if the response indicates failure.

        Example:
            >>> tape_library = TapeLibrary(commcell_object)
            >>> properties = tape_library._get_library_properties()
            >>> print(properties)
            >>> # Access specific property
            >>> location = properties.get('location')
            >>> print(f"Library location: {location}")

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._library_properties_service
        )

        if flag:
            if response.json():
                if 'libraryInfo' in response.json():
                    return response.json()['libraryInfo']
                raise SDKException('Storage', '102', 'Failed to get tape Library properties')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)


    def refresh(self) -> None:
        """Reload the properties and state information for this tape library.

        This method updates the tape library's properties by fetching the latest information,
        ensuring that any changes made externally are reflected in the current object.

        Example:
            >>> tape_library = TapeLibrary()
            >>> tape_library.refresh()
            >>> print("Tape library properties refreshed successfully")

        #ai-gen-doc
        """
        self.library_properties = self._get_library_properties()


    @property
    def library_name(self) -> str:
        """Get the name of the tape library as a read-only property.

        Returns:
            The name of the tape library as a string.

        Example:
            >>> tape_library = TapeLibrary()
            >>> name = tape_library.library_name  # Access the library name property
            >>> print(f"Tape library name: {name}")
        #ai-gen-doc
        """
        return self._name

    @property
    def library_id(self) -> str:
        """Get the unique identifier (ID) of the tape library as a read-only property.

        Returns:
            str: The unique library ID.

        Example:
            >>> tape_library = TapeLibrary()
            >>> lib_id = tape_library.library_id  # Access the library ID property
            >>> print(f"Tape library ID: {lib_id}")

        #ai-gen-doc
        """
        return self._library_id
    
    # === Media Handling Methods ===
    def verify_media_status(self, barcode_list, verify_status=None):
        """
        Verify media status

        Args:
            barcode_list (list[str])   -   barcode that needs to check status.
        """
        for barcode in barcode_list:
            if not self.media_details or not self.latest_media_details:
                self._get_all_media_details()
            
            barcode_details = self.media_details.get(barcode, "")
            if not barcode_details:
                raise SDKException('Storage', '102', f"Failed to check media details for Media BarCode: {barcode}")
            status = barcode_details.get("status")
            if verify_status.lower() != status.lower():
                raise SDKException('Storage', '102', f"Failed to verify media status {barcode}!")
        return True

    def _process_media_details(self, media_details_list):
        """
        Process media details for all media and set media details. 
        """
        self.media_details = {}
        for obj in media_details_list:
            media_barcode = obj.get("barcode")
            if not media_barcode:
                raise SDKException('Storage', '102', "API Response failure, empty BarCode is being returned!!")
            
            # Note - Other required details can be fetched as needed later and getter methods can be set. 
            self.media_details[media_barcode] = {
                "mediaId": obj.get("mediaId"),
                "status": obj.get("status")
            }
        self.latest_media_details = True

    # Getter Methods.
    def _get_all_media_details(self, filter_media_type="all", is_exported="0"):
        """
        Calls v4 API to fetch all media details. 
        Args:
            **kwargs
                -- filterMeidaType = [all, spare, cleaning, retired, overwirte_protected, assigned, exported]
                -- isExported      = (0, 1) 
        """
        url = self._services['MEDIA_IN_TAPE'] % (self.library_id, filter_media_type, is_exported)
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', url)
        
        if flag:
            if response.json():
                response = response.json()
                if len(response.get("mediaDetailsList", [])) > 0:
                    media_details = response.get("mediaDetailsList", [])
                    self._process_media_details(media_details)
                elif "errorCode" in response:
                    error_message = response['errorMessage']
                    o_str = 'Failed to fetch Media details\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                else:
                    raise SDKException('Storage', '102', f"Unknown error - {response}")
            else:
                raise SDKException('Storage', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Storage', '102', f"v4 API error - {response_string}")

    def get_media_status(self, barcode):
        """
        Returns media status

        Args:
            barcode (str)   -   barcode that needs to check status.
        """
        if not self.media_details or not self.latest_media_details:
            self._get_all_media_details()
        
        barcode_details = self.media_details.get(barcode, "")
        if not barcode_details:
            raise SDKException('Storage', '102', f"Failed to check media details for Media BarCode: {barcode}. Please check if barcode is present in library.")
        status = barcode_details.get("status")
        if not status:
            raise SDKException('Storage', '102', f"Could not get status for: {barcode} media!!!!")
        return status
    
    def _get_media_id_list(self, barcode_list):
        """
        Returns list of media Ids.

        Args:
            barcode_list (list[int])   -   barcode ids to be fetched. 
        """
        if not self.media_details or not self.latest_media_details:
            self._get_all_media_details()

        media_id_list = []
        for barcode in barcode_list:
            if barcode not in self.media_details:
                raise SDKException('Storage', '102', f"Media: {barcode} not in library. Please check manually.")
            media_id_list.append(self.media_details.get(barcode).get("mediaId"))

        return media_id_list
            

    def _perform_drive_operation(self, driveId: int, operation: int):
        """
        Common function to perform operation on drive. 
        Supported Operations - 
            - UNLOAD_DRIVE = 0
            - GET_MEDIA_INFO_VALIDATE_DRIVE = 1
            - RESET_DRIVE = 2
            - REPLACE_DRIVE = 3
            - MARK_DRIVE_CLEAN = 4
            - MARK_DRIVE_FIXED = 5

        Args: 
            driveId(int)    -   drive Id to be unloaded.
            operation(int)  -   valid operation to be performed. 
        """
        url = self._services['DRIVE_OPERATION']
        
        payload = {
            "driveId": driveId,
            "driveOperationType": operation
            }
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', url, payload)

        if flag:
            if response.json():
                response = response.json()
                if response.get("errorCode") == 0:
                    return True

                elif "errorCode" in response:
                    error_message = response['errorMessage']
                    o_str = f"Failed perform operation {operation} \nError: {error_message}"
                    raise SDKException('Storage', '102', o_str)
                else:
                    raise SDKException('Storage', '102', f"Unable to perform media operation, Error - {response}")
            else:
                raise SDKException('Storage', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Storage', '102', f"Perform operation failed, Error - {response_string}")

    def _perform_media_operations(self, media_id_list, operation):
        """
        Common function to perform media operations. 
        Supported Operations - 
            - DISCOVER_MEDIA
            - MARK_MEDIA_GOOD
            - MARK_MEDIA_BAD
            - MARK_MEDIA_FULL
            - MARK_MEDIA_ERASABLE
            - MARK_MEDIA_APPENDABLE
            - MARK_MEDIA_REUSABLE
            - PREVENT_MEDIA_REUSE
            - ALLOW_MEDIA_REUSE
            - QUICK_ERASE_SELECTED_MEDIA
            - FULL_ERASE_SELECTED_MEDIA
            - DELETE_MEDIA
            - DELETE_CONTENTS
            - UPDATE_BARCODE
            - MOVE_MEDIA

        Args:
            media_id_list (list[int])   -   list of media ids for which operation needs to be performed. 
            operation (str)             -   operation name tag to be performed. 
        """
        url = self._services['MEDIA_OPERATION'] % (self.library_id)
        
        payload = {
            "operationType": operation,
            "mediaList": media_id_list
            }
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', url, payload)

        if flag:
            if response.json():
                response = response.json()
                if response.get("errorCode") == 0:
                    return True

                elif "errorCode" in response:
                    error_message = response['errorMessage']
                    o_str = f"Failed perform operation {operation} \nError: {error_message}"
                    raise SDKException('Storage', '102', o_str)
                else:
                    raise SDKException('Storage', '102', f"Unable to perform media operation, Error - {response}")
            else:
                raise SDKException('Storage', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Storage', '102', f"Perform operation failed, Error - {response_string}")
    
    def unload_drive(self, drive_id):
        """
        Performs Unload drive operation.

        Args:
            drive Id (int)   -   drive Id for which operations is to be performed.
        """
        self._perform_drive_operation(drive_id, 0)

    def mark_media_appendable(self, barcode_list):
        """
        Marks the barcodes appendable.

        Args:
            barcode_list (list[str])   -   barcodes that needs to be marked appendable.
        """
        media_id_list = self._get_media_id_list(barcode_list)
        self._perform_media_operations(media_id_list, 'MARK_MEDIA_APPENDABLE')
        self.latest_media_details = False
        self.verify_media_status(barcode_list, 'Appendable Media')

    def mark_media_full(self, barcode_list):
        """
        Marks the barcode full

        Args:
            barcode (list[str])   -   barcodes that needs to be marked full.
        """
        media_id_list = self._get_media_id_list(barcode_list)
        self._perform_media_operations(media_id_list, 'MARK_MEDIA_FULL')
        self.latest_media_details = False
        self.verify_media_status(barcode_list, 'Full Media')
    
    # === Media Handling Methods Complete ===
