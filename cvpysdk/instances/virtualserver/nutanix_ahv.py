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

"""File for operating on a Virtual Server Nutanix AHV Instance.

nutanixinstance is the only class defined in this file.

nutanixinstance:            Derived class from VirtualServer
                            Base class, representing a Nutanix AHV
                            instance, and to perform operations on that
                            instance

    __init__(self, agent,_name,iid)   	 --   initialize object of Nutanix AHV
                                              Instance object associated with the
                                              VirtualServer Instance

    _get_instance_properties()           --  VirtualServer Instance class method
                                             overwritten to get nutanix AHV
                                            Specific instance properties as well

    _get_instance_properties_json()		 --  get the all instance related
                                                properties of this subclient.

"""

from ..vsinstance import VirtualServerInstance
from ...exception import SDKException
from ...instance import Instance


class nutanixinstance(VirtualServerInstance):
    """Class for representing Nutanix AHV instance of the Virtual Server agent"""

    def __init__(self, agent, name, iid):
        """ Initialize the Instance object for the given Virtual Server instance

            Args:
                agent               (object)    --  the instance of the agent class

                name                (str)       --  the name of the instance

                iid                 (int)       --  the instance id

        """
        self._nutanix_cluster = None
        self._username = None
        self._server_name = []
        self._vendor_id = 601
        super(nutanixinstance, self).__init__(agent, name, iid)

    def _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(nutanixinstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._nutanix_cluster = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']

            self._username = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['userName']

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
                    "vmwareVendor": {}
                }
            }
        }
        return instance_json

    @property
    def server_host_name(self):
        """
        return the associated clients with the instance
        """
        return self._server_name

    @property
    def nutanix_cluster(self):
        """
        returns the nutanix cluster of the instance

        """
        return self._nutanix_cluster

    @property
    def username(self):
        """
        returns the username of the nuatnix cluster
        """
        return self._username
