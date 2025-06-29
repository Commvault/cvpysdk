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

VirualServerInstance is the only class defined in this file.

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
from inspect import getmembers, isclass, isabstract

from ..instance import Instance
from ..constants import VsInstanceType
from ..exception import SDKException


class VirtualServerInstance(Instance):
    """Class for representing an Instance of the Virtual Server agent."""

    def __new__(cls, agent_object, instance_name, instance_id=None):
        """Decides which instance object needs to be created"""

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

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        super(VirtualServerInstance, self)._get_instance_properties()

        self._vsinstancetype = None
        self._asscociatedclients = None
        if 'virtualServerInstance' in self._properties:
            self._virtualserverinstance = self._properties["virtualServerInstance"]
            self._vsinstancetype = self._virtualserverinstance['vsInstanceType']
            self._asscociatedclients = self._virtualserverinstance['associatedClients']

    def _get_instance_proxies(self):
        """
                get the list of all the proxies on a selected instance

                Returns:
                    instance_proxies   (List)  --  returns the proxies list
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

    def _get_application_properties(self):
        """Gets the application properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
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


    def _update_hypervisor_credentials(self, credential_json):
        """updates the credential for   this instance.

             Args:
                credentialid (int)  --  Credential ID to update in hypervisor
                credentialname(str) -- Credential name to update in hypervisor

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
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
    def server_name(self):
        """returns the PseudoClient Name of the associated isntance"""
        return self._agent_object._client_object.client_name

    @property
    def associated_clients(self):
        """Treats the clients associated to this instance as a read-only attribute."""
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
    def associated_clients(self, clients_list):
        """sets the associated clients with Client Dict Provided as input

            it replaces the list of proxies in the GUI

        Args:
                clients_list:    (list/str)       --- list of clients or client groups

        Raises:
            SDKException:
                if response is not success

                if input is not string or list of strings

                if input is not client of CS
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
                    }
                    ]
                }
            }
        }
        self._commcell_object.qoperation_execute(request_json)
        self.refresh()

    @property
    def co_ordinator(self):
        """Returns the Co_ordinator of this instance it is read-only attribute"""
        if self.associated_clients is not None:
            _associated_clients = self.associated_clients
            associated_client = _associated_clients[0]
            if self._commcell_object.clients.has_client(associated_client):
                return associated_client
            elif self._commcell_object.client_groups.has_clientgroup(associated_client):
                associated_client_group = self._commcell_object.client_groups.get(associated_client)
                return associated_client_group._associated_clients[0]

    @property
    def frel(self):
        """
        Returns the FREL associated at the instance level
            Returns:
                string : frel client name

            Raises:
                SDKException:
                    if failed to fetch properties

                    if response is empty

                    if response is not success
        """
        _application_instance = self._services['APPLICATION_INSTANCE'] % self._instance_id
        flag, response = self._cvpysdk_object.make_request('GET', _application_instance)
        if flag:
            if response.json():
                return response.json().get('virtualServerInfo', {}).get('defaultFBRUnixMediaAgent', {}).get(
                    'mediaAgentName')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @frel.setter
    def frel(self, frel_client):
        """sets the FREL in the instance provided as input
        Args:
                frel_client:    (string)       --- FREL client to be set as FREL

        Raises:
            SDKException:
                if response is not success

                if input is not string

                if input is not client of CS
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
