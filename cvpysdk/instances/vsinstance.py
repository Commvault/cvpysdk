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

"""File for operating on a Virtual Server Instance.

VirtualServerInstance is the only class defined in this file.

VirtualServerInstance: Derived class from Instance Base class, representing a
                            virtual server instance, and to perform operations on that instance

VirtualServerInstance:

     __new__                    --  Decides which instance object needs to be created

    __init__                    --  initialise object of vsinstance class associated with
                                            the specified agent, instance name and instance id

    _get_instance_properties()  --  Instance class method overwritten to add virtual server
                                        instance properties as well

    associated_clients                --  getter or setter for the associated clients

    co_ordinator                    --  getter

    frel                            --  setter or getter for the FREL client

To add a new Virtual Instance, create a class in a new module under virtualserver sub package

The new module which is created has to named in the following manner:
1. Name the module with the name of the Virtual Server without special characters
2.Spaces alone must be replaced with underscores('_')

For eg:
    The Virtual Server 'Red Hat Virtualization' is named as 'red_hat_virtualization.py'
    The Virtual Server 'Hyper-V' is named as 'hyperv.py'
"""

from __future__ import unicode_literals

import re

from importlib import import_module
from inspect import getmembers, isabstract, isclass

from ..instance import Instance
from ..constants import VsInstanceType
from ..exception import SDKException

from typing import TYPE_CHECKING, List, Union
if TYPE_CHECKING:
    from ..agent import Agent


class VirtualServerInstance(Instance):
    """
    Represents an instance of the Virtual Server agent.

    This class provides a comprehensive interface for managing and interacting with
    virtual server instances. It includes methods for retrieving and updating instance
    properties, managing associated clients, handling application-specific properties,
    and updating hypervisor credentials. The class also exposes several properties
    for accessing key instance attributes such as server name, coordinator, and FREL (File Recovery Enabler for Linux).

    Key Features:
        - Creation of virtual server instance objects
        - Retrieval of instance properties and proxies
        - Access to application-specific properties
        - Management of associated clients
        - Update of hypervisor credentials using JSON input
        - Properties for server name, coordinator, FREL, and associated clients

    #ai-gen-doc
    """

    def __new__(cls, agent_object: 'Agent', instance_name: str, instance_id: int = None) -> 'VirtualServerInstance':
        """Create and return an appropriate VirtualServerInstance object.

        This method determines and instantiates the correct subclass of VirtualServerInstance
        based on the provided agent object, instance name, and optional instance ID.

        Args:
            agent_object: The agent object associated with the virtual server instance.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance.

        Returns:
            An instance of VirtualServerInstance or its appropriate subclass.

        #ai-gen-doc
        """

        try:
            instance_name = VsInstanceType.VSINSTANCE_TYPE[agent_object.instances._vs_instance_type_dict[instance_id]]
        except KeyError:
            instance_name = re.sub('[^A-Za-z0-9_]+', '', instance_name.replace(" ", "_"))

        try:
            instance_module = import_module("cvpysdk.instances.virtualserver.{}".format(instance_name))
        except ImportError:
            instance_module = import_module("cvpysdk.instances.virtualserver.null")

        classes = getmembers(instance_module, lambda m: isclass(m) and not isabstract(m))

        for name, _class in classes:
            if issubclass(_class, VirtualServerInstance) and _class.__module__.rsplit(".", 1)[-1] == instance_name:
                return object.__new__(_class)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this virtual server instance.

        This method fetches the latest properties for the current virtual server instance
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        #ai-gen-doc
        """
        super(VirtualServerInstance, self)._get_instance_properties()

        self._vsinstancetype = None
        self._asscociatedclients = None

        if 'virtualServerInstance' in self._properties:
            self._virtualserverinstance = self._properties["virtualServerInstance"]
            self._vsinstancetype = self._virtualserverinstance['vsInstanceType']
            self._asscociatedclients = self._virtualserverinstance['associatedClients']
        if 'credentialEntity' in self._properties:
            self._credential = self._properties['credentialEntity']
            if self._credential.get('credentialName', None):
                try:
                    credential_obj = self._commcell_object.credentials.get(self._credential['credentialName'])
                    self._credential['userName'] = credential_obj.credential_user_name
                except SDKException:
                    self._credential['userName'] = ''

    def _get_instance_proxies(self) -> list:
        """Retrieve the list of all proxies associated with the selected virtual server instance.

        Returns:
            list: A list containing the proxies configured for this instance.

        #ai-gen-doc
        """
        instance_members = self.associated_clients
        instance_proxies = []
        for member in instance_members:
            if self._commcell_object.client_groups.has_clientgroup(member):
                client_group = self._commcell_object.client_groups.get(member)
                clients_obj = self._commcell_object.clients
                instance_proxies.extend(list(set(clients_obj.virtualization_access_nodes).intersection(
                    set(clients.lower() for clients in client_group.associated_clients))))
            else:
                instance_proxies.append(member)

        return list(dict.fromkeys(instance_proxies))

    def _get_application_properties(self) -> None:
        """Retrieve the application properties for this virtual server instance.

        This method fetches the configuration and settings specific to the application
        associated with the current virtual server instance.

        Returns:
            None

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        #ai-gen-doc
        """
        self._APPLICATION = self._services['APPLICATION_INSTANCE'] % (self._instance_id)
        self._application_properties = None

        # skip GET instance properties api call if instance id is 1
        if not int(self.instance_id) == 1:
            flag, response = self._cvpysdk_object.make_request('GET', self._APPLICATION)

            if flag:
                if response.json() and "virtualServerInfo" in response.json():
                    self._application_properties = response.json()["virtualServerInfo"]
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))

    def _update_hypervisor_credentials(self, credential_json: dict) -> None:
        """Update the hypervisor credentials for this virtual server instance.

        Args:
            credential_json: A dictionary containing the credential information to update in the hypervisor.
                Expected keys include:
                    - 'credentialid' (int): The credential ID to update.
                    - 'credentialname' (str): The credential name to update.

        Raises:
            SDKException: If the response from the update operation is empty or indicates failure.

        #ai-gen-doc
        """
        self._credential_service = self._services['INSTANCE_CREDENTIALS'] % int(
                                                                self._agent_object._client_object.client_id)

        # skip GET instance properties api call if instance id is 1
        if not int(self.instance_id) == 1:
            flag, response = self._cvpysdk_object.make_request('PUT', self._credential_service, credential_json)

            if flag:
                if response.json():
                    if 'response' in response.json():
                        if 'errorCode' in response.json()['response']:
                            error_code = response.json()['response']['errorCode']
                            if error_code != 0:
                                error_string = response.json()['response']['errorString']
                                o_str = 'Failed to update credentials\nError: "{0}"'.format(error_string)
                                raise SDKException('Instance', '102', o_str)
                            if 'errorMessage' in response.json():
                                error_string = response.json()['errorMessage']
                                if error_string != "":
                                    o_str = 'Failed to update credentials\nError: "{0}"'.format(error_string)
                                    raise SDKException('Instance', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def server_name(self) -> str:
        """Get the PseudoClient name associated with this virtual server instance.

        Returns:
            The name of the PseudoClient as a string.

        #ai-gen-doc
        """
        return self._agent_object._client_object.client_name

    @property
    def associated_clients(self) -> List[str]:
        """Get the list of clients associated with this virtual server instance as a read-only property.

        Returns:
            List of client names (as strings) associated with the virtual server instance.

        #ai-gen-doc
        """
        self._associated_clients = []
        if "memberServers" in self._asscociatedclients:
            for client in self._asscociatedclients["memberServers"]:
                if 'clientName' in client['client']:
                    self._associated_clients.append(client["client"]["clientName"])
                elif 'clientGroupName' in client['client']:
                    self._associated_clients.append(client["client"]["clientGroupName"])
                else:
                    raise SDKException('Subclient', '102', "No Client Name or Client Group Name in JSON ")
            return self._associated_clients

    @associated_clients.setter
    def associated_clients(self, clients_list: Union[List[str], str]) -> None:
        """Set the associated clients for the Virtual Server Instance.

        This method replaces the current list of proxies in the GUI with the provided clients or client groups.

        Args:
            clients_list: A list of client names or client group names, or a single client/group name as a string.

        Raises:
            SDKException: If the response is not successful, if the input is not a string or list of strings,
                or if the input does not correspond to a valid client of the CommServe.

        #ai-gen-doc
        """
        if not isinstance(clients_list, list):
            clients_list = [clients_list]
        if not isinstance(clients_list, list):
            raise SDKException('Instance', '101')
        for client_name in clients_list:
            if not isinstance(client_name, str):
                raise SDKException('Instance', '105')

        client_json_list = []

        for client_name in clients_list:
            common_json = {}
            final_json = {}
            if self._commcell_object.clients.has_client(client_name):
                common_json['clientName'] = client_name
                common_json['_type_'] = 3
                final_json['client'] = common_json
            elif self._commcell_object.client_groups.has_clientgroup(client_name):
                common_json['clientGroupName'] = client_name
                common_json['_type_'] = 28
                final_json['client'] = common_json
            else:
                raise SDKException('Instance', '105')

            client_json_list.append(final_json)

        request_json = {
            'App_UpdateInstancePropertiesRequest': {
                'instanceProperties': {
                    'virtualServerInstance': {
                        'associatedClients': {"memberServers": client_json_list}
                    }
                },
                'association': {
                    'entity': [{
                        'instanceId': self.instance_id,
                        '_type': 5
                    }]
                }
            }
        }
        self._commcell_object.qoperation_execute(request_json)
        self.refresh()

    @property
    def co_ordinator(self) -> str:
        """Get the coordinator of this virtual server instance.

        This property provides the name or identifier of the coordinator associated with the instance.
        The coordinator is a read-only attribute and cannot be modified directly.

        Returns:
            str: The coordinator of the virtual server instance.

        #ai-gen-doc
        """
        if self.associated_clients is not None:
            _associated_clients = self.associated_clients
            associated_client = _associated_clients[0]
            if self._commcell_object.clients.has_client(associated_client):
                return associated_client
            elif self._commcell_object.client_groups.has_clientgroup(associated_client):
                associated_client_group = self._commcell_object.client_groups.get(associated_client)
                return associated_client_group._associated_clients[0]

    @property
    def frel(self) -> str:
        """Get the FREL (File Recovery Enabler for Linux) client name associated at the instance level.

        Returns:
            The name of the FREL client as a string.

        Raises:
            SDKException: If fetching the FREL properties fails, the response is empty, or the response is not successful.

        #ai-gen-doc
        """
        _application_instance = self._services['APPLICATION_INSTANCE'] % self._instance_id
        flag, response = self._cvpysdk_object.make_request('GET', _application_instance)
        if flag:
            if response.json():
                return response.json().get('virtualServerInfo', {}).get(
                    'defaultFBRUnixMediaAgent', {}).get('mediaAgentName')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @frel.setter
    def frel(self, frel_client: str) -> None:
        """Set the File Recovery Enabler for Linux (FREL) client for this virtual server instance.

        Args:
            frel_client: The name of the FREL client to be set for the instance.

        Raises:
            SDKException: If the response is not successful, if the input is not a string,
                or if the input is not a valid client of the CommServe.

        #ai-gen-doc
        """
        recovery_enablers = self._services['RECOVERY_ENABLERS']
        flag, response = self._cvpysdk_object.make_request('GET', recovery_enablers)
        if flag:
            if response.json():
                frel_ready_ma = response.json().get('mediaAgentList')
                if list(filter(lambda ma: ma['mediaAgentName'].lower() == frel_client.lower(), frel_ready_ma)):
                    _application_instance = self._services['APPLICATION_INSTANCE'] % self._instance_id
                    flag, response = self._cvpysdk_object.make_request('GET', _application_instance)
                    if flag:
                        if response.json():
                            _json = response.json()
                            if _json.get('virtualServerInfo', {}).get('defaultFBRUnixMediaAgent', {}):
                                _json['virtualServerInfo']['defaultFBRUnixMediaAgent']['mediaAgentName'] = frel_client
                            else:
                                raise SDKException('Instance', '102',
                                                   'Not possible to assign/add FREL MA. Please check if the '
                                                   'instance supports FREL')
                            if _json.get('virtualServerInfo', {}).get('defaultFBRUnixMediaAgent', {}).get(
                                    'mediaAgentId'):
                                del _json['virtualServerInfo']['defaultFBRUnixMediaAgent']['mediaAgentId']
                            _json = {'prop': _json}
                            _application_upate = self._services['APPLICATION']
                            flag, response = self._cvpysdk_object.make_request('POST', _application_upate, _json)
                            if not flag:
                                raise SDKException('Response', '102')
                        else:
                            raise SDKException('Response', '102')
                    else:
                        raise SDKException('Instance', '105')
                else:
                    raise SDKException('Instance', '108')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))
