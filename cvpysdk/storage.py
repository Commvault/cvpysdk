# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

    media_agent_name()                      --  returns media agent name

    media_agent_id()                        --  returns media agent id

    is_online()                             --  returns True is media agent is online

    platform()                              --  returns os info of the media agent

    refresh()                               --  refresh the properties of the media agent

    change_index_cache()                    --  runs catalog migration

    index_cache_path()                      --  returns index cache path of the media agent

    index_cache_enabled()                   --  returns index cache enabled status

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

    add_mount_path()            --  adds the mount path on the local/ remote machine

    _get_library_properties()   --  gets the disk library properties

DiskLibrary instance Attributes

    **media_agents_associated**  --  returns the media agents associated with the disk library


"""
from __future__ import absolute_import
from __future__ import unicode_literals
import uuid

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

    def add(self, library_name, media_agent, mount_path, username="", password="", servertype=0):
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
                "opType": 1
            }
        }

        if servertype > 0:
            request_json["library"]["serverType"] = servertype
            request_json["library"]["isCloud"] = 1
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
    def mount_path(self):
        """Treats the library id as a read-only attribute."""
        return self.mountpath

    @property
    def media_agent(self):
        """Treats the library id as a read-only attribute."""
        return self.mediaagent

    def shareMountpath(self, newMA, newmountpath):
        """
        method to specify share mountpath to a disklibrary
        """
        self._EXECUTE = self._commcell_object._services['EXECUTE_QCOMMAND']
        self.library = {
            "opType": 64,
            "mediaAgentName": "%s" %
                              self.mediaagent,
            "libraryName": "%s" %
                           self.library_name,
            "mountPath": "%s" %
                         self.mountpath}
        self.libNewprop = {
            "deviceAccessType": 22,
            "password": "",
            "loginName": "",
            "mediaAgentName": newMA,
            "mountPath": "{}".format(newmountpath),
            "proxyPassword": ""}
        request_json = {
            "EVGui_ConfigureStorageLibraryReq":
                {
                    "library": self.library,
                    "libNewProp": self.libNewprop
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