#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Instance.

VirualServerInstance is the only class defined in this file.

VirtualServerInstance:  Derived class from Instance Base class, representing a
                            virtual server instance, and to perform operations on that instance

VirtualServerInstance:

    _get_instance_properties()              --  Instance class method overwritten to add virtual
                                                    server instance properties as well

    _prepare_instance_json()                --  request json for updating Virtual server Instance
                                                    properties

    _update_instance_properties_request()   --  update the Instance properties with request json

    _vendor_id()                            --  Vendor ID Corresponds to hypervisor

    _default_FBRWindows_MediaAgent()        --  Setter for Default FBR Windows Media Agent property

    _default_FBRWindows_MediaAgent()        --  Setter for Default unix Media Agent property

    _vcPassword()                           --  Setter for VCenter password credentials Property

    _appId()                                --  Getter for Association property

    _docker()                               --  Setter for docker property

    _open_stack()                           --  Setter for Open Stack property

    _azure                                  --  Setter for Azure property

    _azure_Resource_Manager                 --  Setter for Azure Resource Manager property

    _oracle_cloud                           --  Setter for oracle Cloud property

    _associated_Member_Server               --  Setter for Associated Member servers property

    _get_instance_common_properties         --  Method for common properties of
                                                    Virtual Server Instance

"""

from __future__ import unicode_literals

from past.builtins import basestring

from ..instance import Instance
from ..client import Client
from ..exception import SDKException
from ..constants import HyperVisor


class VirtualServerInstance(Instance):
    """Class for representing an Instance of the Virtual Server agent."""

    def __new__(cls, agent_object, instance_name, instance_id=None):
        """Initializes the Instance object for the given Virtual Server instance.

            Args:
                agent_object        (object)    --  instance of the Agent class

                instance_name       (str)       --  name of the instance

                instance_id         (str)       --  id of the instance
                    default: None

            Returns:
                object  -   instance of the Hypervisor instance,
                                if present in the HyperVisorType class
                                otherwise a new object
        """
        if instance_name == HyperVisor.MS_VIRTUAL_SERVER:
            from virtualserver.hypervinstance import HyperVInstance
            return object.__new__(HyperVInstance)
        else:
            return object.__new__()

    def __init__(self, agent_object, instance_name, instance_id):
        """Initializes the Instance object for the given Virtual Server instance.

            Args:
                agent_object        (object)    --  instance of the Agent class

                instance_name       (str)       --  name of the instance

                instance_id         (str)       --  id of the instance
                    default: None

            Returns:
                object  -   instance of the VirtualServerInstance class

        """
        super(VirtualServerInstance, self).__init__(agent_object, instance_name, instance_id)

        self._properties_dict = {}
        self._UPDATE_INSTANCE = self._commcell_object._services['INSTANCE'] % (self.instance_id)

    def _vendor_id(self, value):
        """setter for Vendor ID attribute in Instance"""
        self._vendorid = int(value)

    def _default_FBRWindows_MediaAgent(self):
        """getter for default FBR Windows Media agent. it is read only attribute"""

        _default_FBR_Windows = {
            "_type_": 11
        }

        return _default_FBR_Windows

    def _default_FBRUnix_MediaAgent(self, value):
        """"setter for Default FBR Unix Media Agent"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._default_FBR_unix = {
            "mediaAgentId": int(value.get("browse_ma_id", "")),
            "_type_": 11,
            "mediaAgentName": value.get("browse_ma", "")
        }

    def _vcPassword(self, value):
        """ setter for Credential tag in Instance Property Json"""
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._vc_password = {
            "userName": value.get("user_name", "")
        }

    def _appId(self):
        """getter for App id tag in Instance Property Json . it is read only attribute"""

        _appid_json = {
            "subclientId": 0,
            "clientId": int(self._agent_object._client_object.client_id),
            "instanceId": int(self._instance_id),
            "instanceName": self._instance_name,
            "apptypeId": int(self._agent_object.agent_id),
            "subclientName": "",
            "applicationName": self._agent_object.agent_name
        }
        return _appid_json

    def _docker(self, value):
        """setter Docker id tag in Instance Property Json"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._docker_json = {
            "serverName": value.get("server_name", ""),
            "credentials": {
                "userName": value.get("user_name", "")
            }
        }

    def _open_stack(self, value):
        """setter for openstack id tag in Instance Property Json"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._openstack_json = {
            "serverName": value.get("server_name", ""),
            "credentials": {
                "userName": value.get("user_name", "")
            }
        }

    def _azure(self, value):
        """setter for the Azure tag in Instance property Json"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._azure_json = {
            "serverName": value.get("server_name", ""),
            "credentials": {
                "userName": value.get("user_name", "")
            }
        }

    def _azure_Resource_Manager(self, value):
        """setter for the Azure RM tag in Instance property Json"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._azure_rm_json = {
            "serverName": value.get("server_name", ""),
            "credentials": {
                "userName": value.get("user_name", "")
            }
        }

    def _oracle_cloud(self, value):
        """setter for the Azure RM tag in Instance property Json"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._oracle_cloud_json = {
            "serverName": value.get("server_name", ""),
            "credentials": {
                "userName": value.get("user_name", "")
            }
        }

    def _associated_Member_Server(self):
        """getter for the associated member server . it is read only attribute"""

        _associated_list = []
        for each_client in self.associated_clients["Clients"]:
            _associated_member_json = {
                "srmReportSet": 0,
                "type": 0,
                "hostName": "",
                "clientName": each_client["client_name"],
                "srmReportType": 0,
                "clientSidePackage": True,
                "clientId": int(each_client["client_id"]),
                "_type_": 3,
                "consumeLicense": True
            }
            _associated_list.append(_associated_member_json)

        return _associated_list

    def _get_instance_common_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        self._associated_clients = None

        if 'virtualServerInstance' in self._properties:
            virtual_server_instance = self._properties["virtualServerInstance"]
            if 'associatedClients' in virtual_server_instance:
                associated_clients = virtual_server_instance['associatedClients']

                self._associated_clients = {
                    'Clients': [],
                    'ClientGroups': []
                }

                for member in associated_clients['memberServers']:
                    client = member['client']

                    if 'clientName' in client:
                        temp_dict = {
                            'client_name': client['clientName'],
                            'client_id': client['clientId']
                        }
                        self._associated_clients['Clients'].append(temp_dict)
                    elif 'clientGroupName' in client:
                        temp_dict = {
                            'client_group_name': client['clientGroupName'],
                            'client_group_id': client['clientGroupId']
                        }
                        self._associated_clients['ClientGroups'].append(temp_dict)
                    else:
                        continue

    def _prepare_instance_json(self):
        """Builds the Instance property Json from getters specified"""

        _request_json = {
            "prop": {
                "lockId": 0,
                "creatFailIndex": 0,
                "creatFullIndex": True,
                "dataCollection": 0,
                "virtualServerInfo": {
                    "hostName": "",
                    "description": "",
                    "vendor": self._vendorid,
                    "virtualCenter": True,
                    "vcloudhostName": "",
                    "virtualCenterIsRegistered": False,
                    "createClientsForAllVms": False,
                    "vcenterWebPluginHost": "",
                    "defaultFBRWindowsMediaAgent": self._default_FBRWindows_MediaAgent(),
                    "defaultFBRUnixMediaAgent": self._default_FBR_unix,
                    "docker": self._docker_json,
                    "appId": self._appId(),
                    "openStack": self._openstack_json,
                    "vcPassword": self._vc_password,
                    "esxServersToMount": [""],
                    "azure": self._azure_json,
                    "azureResourceManager": self._azure_rm_json,
                    "oracleCloud": self._oracle_cloud_json,
                    "associatedMemberServer": self._associated_Member_Server()
                },
                "appId": self._appId()
            }
        }
        return _request_json

    def _update_instance_properties_request(self, request_json):
        """
        receives the request json and make update Instance properties request

        args:
            request_json  : Makes request to update isntance property with request json

        exception:
            raise SDK Exception if
                response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._UPDATE_INSTANCE, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']

                    o_str = 'Failed to Update Instance Property\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Instance', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def vs_instance_type(self):
        """Treats the vs instance type as a read-only attribute."""
        return self._vs_instance_type

    @property
    def server_name(self):
        """Treats the v-center name as a read-only attribute."""
        return self._server_name

    @property
    def associated_clients(self):
        """Treats the clients associated to this instance as a read-only attribute."""

        return self._associated_clients

    @associated_clients.setter
    def associated_clients(self, client_name):
        """sets the associated clients with Client Dict Provided as input

        Args:
                client_name:    (str)       --- client_name which needed to be added as proxy

        Raises:
            SDKException:
                if response is not success

                if input is not str

                if input is not client of CS
        """

        _client_dict = {}
        if isinstance(client_name, Client):
            client = client_name
        elif isinstance(client_name, str):
            client = Client(self._commcell_object, client_name)
        else:
            raise SDKException('Subclient', '105')

        _client_dict["client_name"] = client.client_name
        _client_dict["client_id"] = client.client_id

        self.associated_clients["Clients"].append(_client_dict)

    @property
    def co_ordinator(self):
        """Returns the Co_ordinator of this instance it is read-only attribute"""
        _associated_clients = self.associated_clients
        return _associated_clients['Clients'][0]

    @property
    def fbr_MA_unix(self):
        """Returns the FBRMA of this instance if associated . it is read only attribute"""
        # no such attribute check it

    @fbr_MA_unix.setter
    def fbr_MA_unix(self, client_name):
        """ sets FBRMA for this instance
        Args:
                client_name:    (str)       --- client_name which needed to be added as proxy

        Raises:
            SDKException:
                if response is not success

                if input is not str

                if input is not client of CS
        """
        if isinstance(client_name, Client):
            client = client_name
        elif isinstance(client_name, basestring):
            client = Client(self._commcell_object, client_name)
        else:
            raise SDKException('Subclient', '105')

        self._properties_dict["browse_ma"] = client.client_name
        self._properties_dict["browse_ma_id"] = client.client_id
