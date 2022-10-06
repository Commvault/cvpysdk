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

"""File for operating on a Virtual Server Amazon Instance.

AmazonInstance is the only class defined in this file.

AmazonInstance: Derived class from VirtualServer  Base class, representing a
                           Amazon instance, and to perform operations on that instance

AmazonInstance:
    __init__(agent_object,instance_name,instance_id)    --  initialize object of amazon Instance
                                                            object associated with the
                                                            VirtualServer Instance

"""

from ..vsinstance import VirtualServerInstance
from ...exception import SDKException
from ...instance import Instance


class AmazonInstance(VirtualServerInstance):
    def __init__(self, agent, name, iid):
        self._vendor_id = 4
        self._server_name = []
        super(AmazonInstance, self).__init__(agent, name, iid)

    def _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(AmazonInstance, self)._get_instance_properties()
        self._server_name = []
        self._initialize_tenant_instance_properties()
        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))

    def _get_instance_properties_json(self):
        """get the all instance related properties of this subclient.

           Returns:
                dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties": {
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "virtualServerInstance": {
                    "vsInstanceType": self._virtualserverinstance['vsInstanceType'],
                    "associatedClients": self._virtualserverinstance['associatedClients'],
                    "vmwareVendor": self._virtualserverinstance['vmwareVendor']
                }
            }
        }

        return instance_json

    @property
    def server_name(self):
        """getter for the domain name in the AWS vendor json"""
        return self._server_name

    @property
    def server_host_name(self):
        """getter for the domain name in the AWS vendor json"""
        return self._server_name

    def _initialize_tenant_instance_properties(self):
        """"
        Initializes the properties if the client is Tenant
        """
        if 'virtualServerInstance' in self._properties.keys():
            if 'enableAdminAccount' in self._properties['virtualServerInstance']['amazonInstanceInfo']:
                if self._properties['virtualServerInstance']['amazonInstanceInfo']['enableAdminAccount']:
                    admin_ins_id = self._properties['virtualServerInstance']['amazonInstanceInfo']['adminInstanceId']
                    _instance = self._services['INSTANCE'] % (admin_ins_id)
                    flag, response = self._cvpysdk_object.make_request('GET', _instance)
                    if flag:
                        if response.json() and "instanceProperties" in response.json():
                            self._admin_properties = response.json()["instanceProperties"][0]
                            if 'virtualServerInstance' in self._admin_properties:
                                self._asscociatedclients = None
                                self._properties['virtualServerInstance']['associatedClients'] =\
                                    self._admin_properties['virtualServerInstance']['associatedClients']
                                self._virtualserverinstance = self._properties["virtualServerInstance"]
                                self._vsinstancetype = self._virtualserverinstance['vsInstanceType']
                                self._asscociatedclients = self._virtualserverinstance['associatedClients']
                        else:
                            raise SDKException('Response', '102')
                    else:
                        raise SDKException('Response', '101', self._update_response_(response.text))
